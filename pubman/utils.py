'''Utility functions for Publication Manager.

Functions:

    set_extra_permissions: generates permissions for models

    is_published: determines if a model object is published for some models

    permission_to_view_Q: returns a django Q object which finds instances of a model
       that user has permission to view.

    permission_to_view_item: determines if user has permission to view model instance

    make_unique_slug: makes a slug for a model instance unique

    credit_list: returns a list of credits/authors for a model instance

    get_link: returns the URL for a WebpageLink instance

    validate_link: checks that a link in a WebpageLink instance is valid 

    set_additional_languages: merges customised pubman languages and LANGUAGES setting

    set_available_languages: finds languages that an article has been translated into     

    get_limit_user_choices_query: gets users who can be given permission to modify a
        model instance on the admin screens

    make_slug_unqiue: makes a slug unique

    action_clone: action on admin list view screen that allows model instances to be cloned
    
    action_publish: action on admin list view screen that publishes model instances and their unpublished contents 

    action_publish_immediately: Same as action_publish but also sets future date_published values to now. 
    
    get_caption: returns caption in given language for a MediaObject or particular Image
'''

from django.db.models import Q
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db.models.fields import CharField
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

import settings
import models


def set_extra_permissions(model_name):
    """Generates permissions so that authorisation to modify or view articles, 
    media objects and stories can be done granularly, i.e. per user.  
    """
    publication_permissions = (
            ('view_unpublished_' + model_name, 'Can view unpublished'),
            ('edit_other_' + model_name, 'Can edit other user items'),
            ('publish_' + model_name, 'Can publish items'),
            )
    return publication_permissions

def is_published(obj):
        """Returns true if publication_stage is set to published and 
        the current date is >= date_published. 
        """
        return obj.publication_stage == 'P' and datetime.now()>=obj.date_published


def permission_to_view_Q(modelname, user=None, treat_as_anonymous=True):
    '''Query that returns all instances of a model which the specified user 
    has permission to view.
 
    Arguments:
 
    modelname: the name of a model that contains publication_stage, 
        date_published and users_who_can_edit_this fields.

    user: generate appropriate query for given user (default=None) 

    treat_as_anonymous: boolean that if True will only return published 
        instances (defaults to True)   
    '''    
    
    if treat_as_anonymous or user.is_anonymous() or not user:
        return Q(publication_stage='P') & \
                 Q(date_published__lte=datetime.now())
    elif user.has_perm('pubman.view_unpublished_' + modelname):
        return Q()
    else:
        return (Q(publication_stage='P') & \
                 Q(date_published__lte=datetime.now())) | \
                 Q(users_who_can_edit_this__id=user.id) 

    
def permission_to_view_item(model_obj, user):
    if model_obj.is_published():
        return True 
    
    if user.has_perm('pubman.view_unpublished_' + model_obj.__class__.__name__.lower()):
        return True
    else: 
        if model_obj.users_who_can_edit_this.filter(id=user.id).count()>0:
            return True
        else:
            return False  
    

def credit_list(obj, number_to_print=0):
    """Returns formatted list of people for bylines.
    
    Implements "et al." and "and". E.g. "Samuel Johnson, Ingrid Bergman and 
    Lucy Stevens."
    
    Arguments:
    obj -- OrderedCredit GenericRelation 
    number_to_print -- Number of credits to list before "et al." or whatever
        settings.OTHER_AUTHORS_TEXT has been set to. If 0, all authors printed.     

    """
    alist = obj.order_by('order')
    len_alist = len(alist)

    if len_alist == 0:      
        writers=u''
    elif len_alist == 1:        
        writers = unicode(alist[0])
    else:
        if number_to_print == 0 or number_to_print >= len(alist):
            second_last_index = len(alist) - 1
            joining_phrase = unicode(_(u' and '))
            last_name = alist[len(alist)-1].__unicode__()
        else:           
            second_last_index = number_to_print
            joining_phrase = u' ' + ugettext(settings.OTHER_AUTHORS_TEXT)
            last_name = ''
                     
        writers = u', '.join([a.__unicode__() \
            for a in alist[0:second_last_index]]) + joining_phrase + \
            last_name

    return writers              

def get_link(value):
    '''Calculates the actual URL for a FurtherReading instance.
    
    Since the FurtherReading link is user-entered, this is designed not to fail. 
    '''
    
    link = value.strip()
    try:
        # try for integer representing Article foreign key
        i = int(link)
        return reverse('pubman.views.article_detail_by_id', args=[i])
    except ValueError:
        pass
    
    # try for slug representing Article URL 
    if link == slugify(link):
        try:
            return reverse('pubman.views.article_detail', args=[link])
        except:
            return None
    
    
    # Check for story
    if link[0:6] == "story:":
        try:
            # check for story by id
            i = int(link[6:])
            return reverse('pubman.views.story_detail_by_id', args=[i])
        except:
            # check for story by slug
            try:
                if  link[6:] == slugify(link[6:]):
                    return reverse('pubman.views.story_detail', args=[link[6:]])
                else:
                    return None
            except ValueError:
                return None

    # check for relative link
    if link[0:6] == "local:":
        return link[6:] 

    # Check if URL (and reconvert to original case)
    if link[0:7] != 'http://' and \
        link[0:8] != 'https://':
        link = 'http://' + link.strip()
    
    validate = URLValidator(verify_exists=False)
    try:
        validate(link)
        return link
    except ValidationError:
        return None

def validate_link(value):
    '''Used by FurtherReading model to validate that a link is to an article, 
    story or URL.
    '''

    error_message = ugettext(u'This is not a valid link. '
        'Examples of valid links are: ' 
        '15, '
        'story:some-slug, '
        'local:/some/relative/url'
        'www.example.com, '
        'http://www.example.com/example.html')

    if not (get_link(value)):
        raise ValidationError(error_message)
        

def set_additional_languages(original_set, additional_set):
    '''Combines two sets of languages. 
    
    Used to combine django system languages and pubman ones.   
    '''
    new_set = original_set
    for language in additional_set:
        try:
            [l[0] for l in original_set].index(language[0])
        except ValueError: 
            new_set += (language,)
           
    return sorted(new_set) 

def set_available_languages(language_tuples, translations, article_language):
    '''Finds all translation languages available for a particular article. 
    '''
    available_languages = ()
    
    for language in ([t.language for t in translations] + [article_language,]):
        try:
            index = [l[0] for l in language_tuples].index(language)
            available_languages += (language_tuples[index],)            
        except ValueError:
            pass
    return available_languages
    
def get_limit_user_choices_query(descriptive_name): 
    """Returns a Q object that will be used to filter the users who may be 
    assigned to edit the calling model. 
    
    This filters out all users who do not have permission to edit the  
    calling model and all users who have permission to edit it
    irrespective of whether or not they are selected from this list.  
    """
    return Q(is_staff=True) & Q(is_superuser=False) &\
         (~Q(groups__permissions__codename='edit_other_'+descriptive_name) &\
         ~Q(user_permissions__codename='edit_other_'+descriptive_name)) &\
         (Q(groups__permissions__codename='change_'+descriptive_name) |\
         Q(user_permissions__codename='change_'+descriptive_name)) 

    
import re
from django.template.defaultfilters import slugify

def make_slug_unique(object):
    '''Generate a unique slug for models inheriting from ContentObject abstract 
    model. 
    '''
    if not object.slug or object.slug == "":
        slug_value = object.title
    else:
        slug_value = object.slug
    _unique_slugify(object, slug_value)


def _unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.
    This is from SmileyChris at http://djangosnippets.org/snippets/690/

    Arguments
    slug_field_name --- should be a string matching the name of the field to
        store the slug in (and the field to check against for uniqueness).
    queryset --- usually doesn't need to be explicitly provided - it'll default
        to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    This is from SmileyChris at http://djangosnippets.org/snippets/690/
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value
    
def _clone_objects(objects, title_fieldnames):
    """Creates and saves deep copies of multiple Model objects.
    
    Based on code taken from: 
    http://www.bromer.eu/2009/05/23/a-generic-copyclone-action-for-django-11/
    I have added some poor code (that works) to this function. It could be 
    improved by a better coder than me.
    
    Arguments:
    objects -- either a single Model object or a list of them
    title_fieldnames -- names of fields that must be given unique values. The 
       text " (copy) " is suffixed to them.     
           
    """
    def clone(from_object, title_fieldnames):
        args = dict([(fld.name, getattr(from_object, fld.name))
                for fld in from_object._meta.fields
                        if fld is not from_object._meta.pk]);

        for field in from_object._meta.fields:
            if field.name in title_fieldnames:
                if isinstance(field, CharField):
                    args[field.name] = getattr(from_object, field.name) + " (copy) "

        return from_object.__class__.objects.create(**args)

    if not hasattr(objects,'__iter__'):
        objects = [ objects ]

    # We always have the objects in a list now
    objs = []
    for object in objects:
        obj = clone(object, title_fieldnames)

        obj.save()
        for field in object._meta.many_to_many:
            source = getattr(object, field.attname)
            destination = getattr(obj, field.attname)
            for item in source.all():
                kwargs = {}
                '''This is a hack in need of an improvement. 
                If destination.add(item) is called for 
                a generic.GenericRelation field like author_or_institution
                then the author is moved from source to destination instead 
                of being copied. I don't understand why this happens. 
                However, using create works.
                I also don't know a generic way to identify a GenericRelation. 
                Nor do I know how to generically build kwargs to pass to create.
                Anyway this works for now. - Nathan 2010/12/14
                '''
                try:
                    kwargs['author_or_institution_id']=getattr(item, 'author_or_institution_id')
                    destination.create(**kwargs)                    
                except AttributeError:
                    try:
                        destination.add(item)
                    except AttributeError:
                        ''' Handle OrderedArticle 'through' table for story.articles.
                        This is slow, besides being an awful hack - Nathan 2011/02/24
                        '''
                        if isinstance(object, models.Story):
                            ordered_article = models.OrderedArticle.objects.get(
                                            story__id=object.id, article__id=item.id)
                            ordered_article.id = None
                            ordered_article.story = obj
                            ordered_article.save()
        obj.save()
#        '''This is a hack for the orderedarticle_set in stories.
#        '''
#        if object.__class__.__name__ == 'story':
#            
#            for orderedarticle in object.orderedarticle_set.all():
#                obj.orderedarticle_set.create(story=orderedarticle.story,
#                                               article=orderedarticle.article,
#                                               order=orderedarticle.order)
#        objs.append(obj)



def action_clone(modeladmin, request, queryset):
    """An action of the list admin screen to copy objects.
    
    Only tested with Article, MediaObject and Story. 
    """
    _clone_objects(queryset, ("name", "title"))

action_clone.short_description = _('Copy the selected items')

def action_publish(modeladmin, request, queryset, immediately=False):
    """An action of the list admin screen to publish ContentObjects.
    
    This version of publish defaults to not change the value of the 
    instance's date_published field unless it is null.
    """
   
    if queryset:
        if request.user.has_perm('publish_' + queryset[0].__class__.__name__.lower()):
            for object in queryset:
                object.publish(immediately)
                # Step through all the fields and call publish on those
                # that are instances of ContentObject.
                # This will, for example, publish the primary_media_object
                # of an Article instance.
                for field in object._meta.fields:
                    attribute_object =  getattr(object, field.name)
                    if isinstance(attribute_object, models.ContentObject):
                        attribute_object.publish(immediately)

action_publish.short_description = _("Publish but don't change publication dates.")

def action_publish_immediately(modeladmin, request, queryset):
    """An action of the list admin screen to publish ContentObjects.
    
    This version of publish forces the date_published field to be 
    now if it is in the future. 
    """
    action_publish(modeladmin, request, queryset, True)

action_publish_immediately.short_description = _("Publish and set publication dates that are in the future to now.")

    
def get_caption(object,
                language,
                fail_silently=True):
    '''Returns the caption for a particular image or MediaObject in the 
    given language. 
    '''    
    try:
        caption = object.captions.get(language=language)
    except ObjectDoesNotExist:
        if fail_silently: 
            return ""
        else:
            raise ValueError
        
    return caption.text
    