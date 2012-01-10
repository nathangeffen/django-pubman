'''Views for pubman.

These are:
    
    media_object_detail: view media objects
    
    article_list_view: called by other views that process article lists
    
    index: suitable frontpage of website view that lists latest published 
        articles with frontpage set to True, ordered by publication date.

    tag_view: lists articles by tag. Can accept complex tag expressions in 
        the url query.
        
    article_detail: the main view for articles. Processes stories and 
        translations for article too.
    
    article_detail_by_id: redirects to article_detail (which takes a slug)
    
    story_detail: story view
    
    story_detail_by_id: redirects to generic detail (which takes a slug)

    edit_profile: user profile create and edit view
    
    search: Implements a search of the website uses Haystack. 
        Tested with Whoosh.
        
    markdownpreview: used to preview markdown textareas
'''

import re
from copy import copy
import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
#from django.db.models import Q
from django.db.models import get_model
from django.template import RequestContext
from django.views.generic import list_detail
from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.contrib import messages

from tagging.models import TaggedItem

from siteconfig.utils import get_setting

from pubman import settings
from pubman.models import Article, MediaObject, Story 
from pubman.models import Translation
from pubman.forms import UserProfileForm, UserForm
from pubman.utils import set_available_languages 

def media_object_detail(request, slug):
    '''View a media object.
    '''

    media_obj = get_object_or_404(MediaObject, slug=slug)
    
    if not media_obj.permission_to_view_item(request.user):
        raise Http404
    
    return list_detail.object_detail(
        request,
        queryset = MediaObject.objects.all(),
        slug = slug,
        extra_context = {'published' : media_obj.is_published()},                                      
    ) 


def article_list_view(request, article_list, 
                      html_template, 
                      published_only=True,
                      paginate_by=get_setting('ARTICLES_PER_PAGE', settings.ARTICLES_PER_PAGE),
                      story=None, 
                      additional_context={}):
    '''View a filtered list of articles. This is called by other
    views listing articles including index and tag_view.
    
    Parameters:
    
        request
        
        html_template: template to use to render this view.
        
        published_only: if true, only published articles will be listed
            (defaults to True)
        
        paginate_by: number of articles per page
            (defaults to PUBMAN_ARTICLES_PER_PAGE setting)
            
        story: story that must be used with this article - set to none
            if there is no story (default=None)
            
        additional_context: dictionary of additional data for template
    '''

    article_list = article_list.\
        filter(Article.permission_to_view_Q(request.user, published_only)).\
            order_by('-sticky', '-date_published')

    paginator = Paginator(article_list, paginate_by)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        articles_for_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        articles_for_page = paginator.page(paginator.num_pages)

    for article in articles_for_page.object_list:
        article.blurb = article.blurb.partition(settings.TEXT_SHORTEN_CODE)[0]

    from_page = max(1, page-5)
    to_page = min(paginator.num_pages, page+5) + 1
     
    page_range = [i for i in range(from_page, to_page)]

    additional_context.update( {
        'page_obj': articles_for_page,
        'page_range' : page_range,
        'story' : story,
        'page' : page
    })
    
    return render_to_response(html_template, 
                              additional_context,
                              context_instance=RequestContext(request))
    
def index(request):
    '''Front page view.'''

    article_list = Article.objects.filter(frontpage=True)
        
    return article_list_view(request, article_list, 
                             'pubman/index.html')


def tag_view(request, 
             tag_expression, 
             app_name = 'pubman',
             model_name='article', 
             view=article_list_view,
             html_template='pubman/tag.html'):
    """This snippet is a view for complex tag queries that generates a list of model instances matching the set expression generated by the tag_expression argument which in my application is from the querystring. It uses the django-tagging app.

E.g. http://example.com/people/?(deceased&parrot)|"Monty Python"
will retrieve all people who are either deceased parrots or members of Monty Python.


In the tag_expression argument:

* ALL is treated as a keyword. If you happen to have a tag called ALL and want to retrieve all objects with it, surround in quotation marks. E.g. "ALL"

* Examples: 

  - famous -returns all instances of the model tagged with famous

  - famous&deceased -returns all instances of the model tagged both famous and deceased.

  - famous|deceased -returns all instances of the model tagged famous or deceased.

  - parrot^deceased -returns all alive parrots in the model. (^ equals subtraction)

  - ALL^deceased -returns all instances of the model that are not tagged deceased.

  - "great author"&deceased -returns all models tagged as great authors and deceased.

Note: This view currently assumes that a tag is composed of letters, digits, underscores and spaces. 
    
Arguments:

* request -- HTTP Request object

* tag_expression -- a set expression of tags, supporting intersection, union, parenthesis and difference

* app_name -- app containing the model 

* model_name -- model on which to apply the set operations (defaults to Article) 

* view -- view to redirect to after the model instance list has been 
constructed 

* html_template -- HTML template to redirect (defaults to 'pubman/tag.html')
"""

    model_filter = TaggedItem.objects.filter(content_type__model=model_name)
    
    search_string = '\'[\w\s-]+\'|\"[\w\s-]+\"|[\w\s-]+|&|\||\(|\)|\^'    
    parse_string = re.findall(search_string, tag_expression)
     
    querystring = ""
     
    for token in parse_string:
        if token in ['&', '|','^', '(',')']:
            if token == '^':
                token = '-'
            querystring +=  ' ' + token + ' '
        elif token == 'ALL':
            querystring += ' set([i.id for i in get_model("' +\
                app_name + '", "' +\
                model_name + '")'+ '.objects.all()])'            
        else:
            token = token.replace('"','')
            token = token.replace("'","")            
            querystring += ' set([i.object_id for i in '+\
                'model_filter.filter(tag__name="' + token + '")])'

    try:                
        instances = eval(querystring)
    except:
        # This is the fallback when there's an error in the expression.
        # A better way might be to raise Http404.
        instances = model_filter.filter(tag__name=tag_expression)

    object_list = get_model(app_name, model_name).\
        objects.all().filter(id__in=instances)
      
    additional_context = {'tag_expression': tag_expression,}        
    return view(request, 
                object_list, 
                html_template, 
                additional_context=additional_context)

@csrf_protect
def article_detail(request, article_slug, article_lang=None):
    '''Article view that also handles translations and stories. The latter are
    specified using the story slug in the URL query line, e.g. 
        /article/a-day-in-the-life/?story=gulag-stories
        
    Translations are indicated in the article_lang argument.
        
    '''
    
    article_obj = get_object_or_404(Article, slug=article_slug)

    # Determine if user has permission to view this article

    if not article_obj.permission_to_view_item(request.user): 
        raise Http404

    if not article_obj.is_published(): 
        messages.info(request, _('This article is unpublished, '
                                 'but you have permission to view it'))

    # Determine if user can moderate the comments on this article
    if request.user.has_perm('comments.can_moderate'):
        can_moderate_comments = True      
    else:
        can_moderate_comments = False

    if request.user.has_perm('pubman.change_article'): 
        if request.user.has_perm('pubman.edit_other_article'):
            user_can_edit = True
        else:
            try:
                article_obj.users_who_can_edit_this.get(id=request.user.id)
                user_can_edit = True
            except ObjectDoesNotExist:        
                user_can_edit = False
    else:
        user_can_edit = False
        

    # Determine if comments are allowed for this article
    if not article_obj.comments_allowed or\
        (settings.COMMENTERS_MUST_BE_AUTHENTICATED and\
        not request.user.is_authenticated()):
        comments_allowed = False
    else:
        comments_allowed = True
 
    # Process translations

    translations = Translation.objects.filter(article__id=article_obj.id).\
        filter(Translation.permission_to_view_Q(request.user, False))
        
    
    available_languages = set_available_languages(settings.ALL_LANGUAGES, 
                                translations,article_obj.language)

    try:
        if article_lang:
            i = [t.language for t in translations].index(article_lang)
            article_obj.title = translations[i].title
            article_obj.subtitle = translations[i].subtitle
            article_obj.blurb = translations[i].blurb
            article_obj.article_text = translations[i].article_text
            article_obj.text_format = translations[i].text_format
            article_obj.primary_pullout_quote = translations[i].\
                primary_pullout_quote 
            translator_list = translations[i].full_author_list()
            translation_date = translations[i].date_published
            translated = True
            if not translations[i].is_published():
                messages.info(request, _('This translation is unpublished, '
                                 'but you have permission to view it'))
        else:
            article_lang = article_obj.language
            translator_list = None
            translation_date = None
            translated = False
    except ValueError:
        raise Http404


    # Remove shorten codes from blurbs
    article_obj.blurb = article_obj.blurb.replace(settings.TEXT_SHORTEN_CODE, "\n")
        
    # Process page breaks for article_text and put sliced up article into list
    # This is not pythonic. Needs improving. 
    print_this = request.GET.get('print', 'false')
    if print_this.strip().lower() == 'true':
        print_this = True
    else:
        print_this = False
    
    article_pages = []
    
    if article_obj.page_break_strategy == 'C' and not print_this: 
        process_text = article_obj.article_text
        index = process_text.find(settings.PAGE_BREAK_CODE)
        while len(process_text) > 0:
            art = copy(article_obj)
            if index > -1:
                art.article_text = process_text[0:index]
                process_text = process_text[index+len(settings.PAGE_BREAK_CODE):]
                index = process_text.find(settings.PAGE_BREAK_CODE)
            else:
                art.article_text = process_text
                process_text = ""
            article_pages.append(art)
    else:
        if print_this:
            article_obj.article_text = article_obj.article_text.replace(settings.PAGE_BREAK_CODE,'')
        article_pages = [article_obj]                

    # Must put something into article_pages, else the template might fall over
    # when the article_text is referenced.
    if len(article_pages)==0:                             
        article_pages = [article_obj,]

        
    paginator = Paginator(article_pages, 1)
     

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    # If page request (9999) is out of range, deliver last page of results.
    try:
        article_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        article_page = paginator.page(paginator.num_pages)

    # Process story

    story_slug = request.GET.get('story', None)
       
    if story_slug:
        try:
            story = Story.objects.get(slug=story_slug)
        except:
            messages.info(request, _('There is no story called ') + story_slug)
            story = None
        else:
            story_articles = Article.\
            objects.filter(orderedarticle__story__id=story.id).distinct().\
                order_by('orderedarticle__order')
            if not request.user.has_perm('pubman.change_article') or\
                not request.user.has_perm('pubman.edit_other_article'): 
                story_articles = story_articles.filter(publication_stage='P', 
                    date_published__lte=datetime.datetime.now())
    else:
        story = None      
        story_articles = None

    # Process further reading
    
    further_reading = article_obj.further_reading.through.objects.filter(
                                            article__id=article_obj.id)

    return render_to_response('pubman/article_detail.html',
        {'object' : article_obj,
         'paginator' : paginator,
         'page_obj': article_page,
         'can_moderate_comments' : can_moderate_comments,
         'comments_allowed': comments_allowed,
         'user_can_edit': user_can_edit,
         'print_this_button' : settings.PRINT_THIS, 
         'print_this' : print_this,
         'story' : story,
         'story_articles' : story_articles,
         'available_languages' : available_languages,
         'article_lang' : article_lang,
         'translated': translated,
         'translator_list': translator_list,
         'translation_date': translation_date,
         'further_reading' : further_reading
        },
        context_instance=RequestContext(request)
     )     


def article_detail_by_id(request, article_id):
    '''Redirect to article_detail using slug
    '''
    article_obj = get_object_or_404(Article, id=article_id)
    return redirect(article_detail, article_obj.slug)

def story_detail(request, story_slug):
    '''View for story.
    '''
    story_obj = get_object_or_404(Story, slug=story_slug)

    #  Set pagination    
    if story_obj.number_of_articles_per_page == 0:
        number_of_articles_per_page = 9999
    elif story_obj.number_of_articles_per_page == -1:
        number_of_articles_per_page = settings.ARTICLES_PER_PAGE
    else:
        number_of_articles_per_page = story_obj.number_of_articles_per_page

    # Get all articles belonging to this story
    article_list = Article.\
        objects.filter(orderedarticle__story__id=story_obj.id).\
        filter(publication_stage='P', date_published__lte=datetime.datetime.now()).\
        distinct().\
        order_by('orderedarticle__order')

    # Set user_can_edit context variable if user has permission to 
    # edit this story         
    if request.user.has_perm('pubman.change_story'): 
        if request.user.has_perm('pubman.edit_other_story'):
            user_can_edit = True
        else:
            try:
                story_obj.users_who_can_edit_this.get(id=request.user.id)
                user_can_edit = True
            except ObjectDoesNotExist:        
                user_can_edit = False
    else:
        user_can_edit = False
            
    return article_list_view(request, 
                             article_list,
                             'pubman/story_detail.html',
                             published_only=False,
                             paginate_by=number_of_articles_per_page,
                             story=story_obj,
                             additional_context={
                                'user_can_edit' : user_can_edit,
                             })

def story_detail_by_id(request, story_id):
    '''Redirects to story view using slug.
    '''
    story_obj = get_object_or_404(Story, id=story_id)
    return redirect(story_detail, story_obj.slug)

######### Override of django-profile create and edit views

@login_required
def edit_profile(request):
    '''Create or edit user profile view.
    '''
    if request.method == 'POST':
        # The forms submitted by the client.
        user_form = UserForm(request.POST, instance=request.user)
        
        try:        
            profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        except ObjectDoesNotExist:
            profile_form = UserProfileForm(request.POST, request.FILES)             

        if user_form.is_valid() and profile_form.is_valid():
            # The forms validated correctly.
            user_form.save()
            profile_form.fields.user = request.user.id 
            profile_form.save()
            # Change this location as necessary.
            return HttpResponseRedirect('/profiles/'+request.user.username)

    else:
        # Initialise the forms.
        user_form = UserForm(instance=request.user)

        try:
            profile_form = UserProfileForm(instance=request.user.userprofile)
  
        except ObjectDoesNotExist:
            profile_form = UserProfileForm()
        

    return render_to_response('profiles/edit_profile.html',
        {'user_form': user_form, 'profile_form': profile_form,},
        context_instance=RequestContext(request)) 


### Haystack raw search view

from haystack.query import SearchQuerySet

SEARCH_RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 50)

def search(request):
    '''View to do a haystack search of the website content. 
    Tested using Whoosh. 
    '''
    try:
        search_string = request.GET['q']
    except KeyError:
        search_string = ""
    
    if search_string:
        search_results = SearchQuerySet().filter(content=search_string) 
        paginator = Paginator(search_results, SEARCH_RESULTS_PER_PAGE)
        page_range = paginator.page_range

        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            object_list = paginator.page(page)
        except (EmptyPage, InvalidPage):
            object_list = paginator.page(paginator.num_pages)

    else:    
        messages.info(request, _('Please enter something to search'))
        object_list = None
        page_range = None
        page = None

    
    return render_to_response('search/search.html', {
                    'query' : search_string,
                    'page' : object_list,
                    'page_range' : page_range,
                    'page_no' : page,
                    }, context_instance=RequestContext(request))



def markdownpreview(request):
    '''Used by Markitup! editor to render the markdown for the preview button.
    '''
    from django.contrib.markup.templatetags.markup import markdown
    data = markdown(request.POST.get('data', ''), settings.MARKDOWN_EXTENSIONS) 
    return render_to_response( 'pubman/markdownpreview.html',
                              {'preview': data,},
                              context_instance=RequestContext(request))


from django.contrib.auth.decorators import user_passes_test
@user_passes_test(lambda u: u.is_superuser)
def clear_cache(request):
    from django.core.cache import cache    
    from django.http import HttpResponse

    cache.clear()
    return HttpResponse(_('The cache has been cleared.'))
    
    
