"""Implements customised admin screens for Publication Manager models.

    Mostly standard but two things users of pubman should be aware of:
        1. If a textarea is given the class "editor", then it is rendered on  
        the admin screen giving users a choice to switch between a tinymce editor,
        markdown editor or plain textarea editor. A text_format select box must 
        also be rendered on the same screen.
        2. Instead of limiting users for the users_who_can_edit_this fields in the
        model, it is done here by setting the kwargs["queryset"] value.
        
    This module could do with some refactoring.  
"""

#from django.contrib.comments import Comment
from django.contrib.comments.models import CommentFlag
from django import forms
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.forms.widgets import HiddenInput

from django.db.models import ImageField, IntegerField

from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail.admin import AdminImageWidget
from sorl.thumbnail.fields import ImageFormField

from pubman.models import PUBLICATION_STAGES

from pubman.models import Copyright
from pubman.models import UserProfile
from pubman.models import Subscription
from pubman.models import MediaObject
from pubman.models import Credit
from pubman.models import OrderedCredit
from pubman.models import Article
from pubman.models import OutOfDate
from pubman.models import HistoricalEdit
from pubman.models import Translation
from pubman.models import FurtherReading
from pubman.models import Story
from pubman.models import OrderedArticle
from pubman.models import FeaturedStory 
from pubman.models import FeaturedWebpageGroup
from pubman.models import WebpageLink
from pubman.models import OrderedWebpage
from pubman.models import FeaturedRSSFeed
from pubman.models import Image
from pubman.models import Caption
from pubman.models import Video

from pubman.utils import get_limit_user_choices_query, action_clone,\
    action_publish, action_publish_immediately

textarea_css = {
    'screen': ('pubman/css/smoothness/jquery-ui-1.8.6.custom.css',
               'pubman/css/wordcount.css',
               'pubman/markitup/skins/markitup/style.css',
               'pubman/markitup/sets/markdown/style.css',),
} 

jquery_js = (
    'pubman/js/jquery-1.4.3.min.js',
    'pubman/js/jquery-ui-1.8.6.custom.min.js',
)

textarea_js = (
    'pubman/js/tiny_mce/tiny_mce.js',   
    #'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
    #'grappelli/tinymce_setup/tinymce_setup.js',                    
    'pubman/js/textareas.js',
    'pubman/markitup/jquery.markitup.js',
    'pubman/markitup/sets/markdown/set.js',        
)

mediaobjectadmin_js = ('pubman/js/mediaobjectadmin.js',)


class OrderedCreditInline(generic.GenericTabularInline):
    classes = ('collapse closed',)
    model = OrderedCredit
    raw_id_fields = ('author_or_institution',)
    related_lookup_fields = {
        'fk': ['author_or_institution'],
    }    
    extra = 0
    verbose_name = _('Credit') 
    sortable_field_name = "order"
    formfield_overrides = {
        IntegerField: {'widget': HiddenInput},
    }    


class FurtherReadingInline(admin.TabularInline):
    classes = ('collapse closed',)    
    model = FurtherReading
    raw_id_fields = ('url',)
    related_lookup_fields = {
        'fk': ['url'],
    }    
    
    extra = 0
    verbose_name = _('Further Reading')
    sortable_field_name = "order"      
    formfield_overrides = {
        IntegerField: {'widget': HiddenInput},
    }    


class ContentObjectAdmin(admin.ModelAdmin):
    '''This is a base class for Admin objects used for models that inherit from
    ContentObject.
    '''
    search_fields = ('title', 'author__author_or_institution__first_names', 
                     'author__author_or_institution__last_name',)
    save_on_top = True    
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ['users_who_can_edit_this', ]
    inlines = [OrderedCreditInline,]
    actions = [action_clone, action_publish, action_publish_immediately]

    modelname = 'contentobject'

    def get_form(self, request, obj=None, **kwargs):
        '''Used to pass the user in the request to the form.
        '''
        form = super(ContentObjectAdmin, self).get_form(request, obj, **kwargs)
        form.user = request.user
        return form

    def formfield_for_manytomany(self, db_field, request, **kwargs): 
        if db_field.name == 'users_who_can_edit_this':
            instance = self.form.model()
            name = instance.__class__.__name__.lower()
            kwargs["initial"]  = [request.user]
            kwargs["queryset"] = User.objects.filter(get_limit_user_choices_query(name)).distinct()             
        return super(ContentObjectAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def queryset(self, request):
        '''Limits to only those users who may edit this or be denied
        authorisation to edit this.
        '''
        instance = self.form.model()
        name = instance.__class__.__name__.lower()
        qs = super(ContentObjectAdmin, self).queryset(request)
        if request.user.has_perm('pubman.edit_other_' + name):
            return qs
        return qs.filter(users_who_can_edit_this__id=request.user.id)
 
class MediaObjectForm(forms.ModelForm):
    model = MediaObject
    class Media:     
        js = jquery_js + mediaobjectadmin_js 


class MediaObjectAdmin(AdminImageMixin, ContentObjectAdmin):    
    form = MediaObjectForm
    list_display = ['id', 'title', 'thumbprint', 'full_author_list',  
                    'copyright', 'media_type', 'publication_stage',]
    list_filter = ('publication_stage', 'media_type', 'copyright', 'tags',)
    raw_id_fields =  ['video_files', 'images', 'captions',]

    related_lookup_fields = {
        'm2m' : ['video_files', 'images', 'captions',]
    }    

    
    fieldsets = (
        (None, {
            'classes': ['wide',],    
            'fields': ('title', 'subtitle', 'media_type',),
        }),
        
        (_('Image on site'), {
         'classes' : ['images-on-site',],
         'fields': ('images',)
        }),

        (_('Video on site'), {
         'classes' : ['video-on-site',],
         'fields': ('video_files', 'preload')
        }),
        
        (_('Embedded image, video, slideshow or map on an external site'), {
         'classes' : ['embedded',],
         'fields': ('embedded',)
        }),

        (_('Add captions'),
         {'classes': ['collapse',],
          'fields': ('captions',),
        }),
        
        (_('Categorise this media by giving it tags'),
         {'classes': ['collapse',],
          'fields': ('tags',),  
        }),
               
        (_('Advanced options'), {
            'classes': ['collapse',],                                 
            'fields': ('date_published',  
                       'publication_stage',
                       'copyright',
                       'notes',
                       'users_who_can_edit_this', 
                       'slug',)
        }),
    )


class ArticleForm(forms.ModelForm):      
    model = Article
    
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
                      
        # Only allow users with the following permission
        # to publish an unpublished article
                          
        if not self.user.has_perm('pubman.publish_article'): 
            try:
                article = kwargs['instance']
            except KeyError:
                article = None
            
            if not article or article.publication_stage != 'P':
                self.fields['publication_stage'].choices = \
                    PUBLICATION_STAGES[0:len(PUBLICATION_STAGES)-1]

    class Media:
        css = textarea_css 
        js = jquery_js +  textarea_js 
    

class ArticleAdmin(ContentObjectAdmin):

    form = ArticleForm

    inlines = [OrderedCreditInline, FurtherReadingInline, ]            
    list_display = ['id', '__unicode__', 'full_author_list', 'date_last_edited', 
                    'date_published', 'publication_stage']
    list_filter = ['publication_stage', 'tags',
                   'date_published', 'date_last_edited', 'copyright']
    raw_id_fields = ('primary_media_object',)
    
    related_lookup_fields = {
        'fk': ['primary_media_object'],
    }    
    
    filter_horizontal = ['users_who_can_edit_this', 'further_reading']    

    fieldsets = (
        (_('Title and subtitle'), {
            'classes': ['collapse open wide',],    
            'fields': ('title', 'subtitle', )
        }),
        (_('Content'),
         {'classes': ['collapse open editor',],
          'fields': ('blurb','article_text',),
        }),
        (_('How text is entered'), {
          'classes': ['collapse closed editor',],                                    
          'fields': ('text_format', )
        }),
        (_('Primary media for this article'),
        {
         'classes': ['collapse open editor',],         
         'fields': ('primary_media_object',),
        }),        
        (_('Categorise this article by giving it tags'),
         {'classes': ['collapse closed',],
          'fields': ('tags',),
        }),                
        (_('Advanced options'), {
            'classes': ['collapse closed',],
            'fields': ('date_published', 
                       'date_originally_published', 
                       'purpose_of_edit',
                       'publication_stage',
                       'primary_pullout_quote',                    
                       'frontpage',
                       'page_break_strategy',
                       'language',
                       'complexity',
                       'subscription_required',
                       'copyright',
                       'notes',
                       'users_who_can_edit_this', 
                       'slug',)
        }),
    )
                            

class TranslationForm(forms.ModelForm):   
    model = Translation
    
    class Media:
        css = textarea_css
        js = jquery_js +  textarea_js 
    

class TranslationAdmin(ContentObjectAdmin):    
    form = TranslationForm
    list_display = ['id', '__unicode__', 'full_author_list', 'date_last_edited', 
                    'date_published', 'publication_stage']
    list_filter = ['publication_stage', 'language',]    
    raw_id_fields = ('article',)
    
    related_lookup_fields = {
        'fk': ['article'],
    }    
            
    fieldsets = (
        (None, {
            'classes': ['wide',],    
            'fields': ('title', 'subtitle', 
                       ('date_published', 
                        'publication_stage'),
                        )
        }),
        (_('Article to which this translation is linked and the language of this translation'),
        {
         'fields': ('article', 'language',),
        }),
        (_('Content in the original article that can be translated'),
         {'classes': ['editor',],
          'fields': ('blurb','article_text','primary_pullout_quote',),
        }),
        (_('Categorise this article by giving it tags'),
         {'fields': ('tags',),
        }),        
        (None, {'fields': ('text_format',)}),
        ('Advanced options', {
            'classes': ['collapse',],
            'fields': ('copyright',
                        'notes',
                       'users_who_can_edit_this', 
                       'slug',)
        }),
    )
                


class OrderedArticleInline(admin.TabularInline):
    model = OrderedArticle
    raw_id_fields = ('article',)
    related_lookup_fields = {
        'fk': ['article'],
    }    
    sortable_field_name = "order"
    formfield_overrides = {
        IntegerField: {'widget': HiddenInput},
    }      

class StoryForm(forms.ModelForm):
    model = Story
    class Media:
        css = textarea_css
        js = jquery_js + textarea_js

class StoryAdmin(ContentObjectAdmin):
    
    form = StoryForm
    inlines = [OrderedCreditInline, OrderedArticleInline, ] 
    list_display = ['id', '__unicode__', 'full_author_list', 'date_last_edited', 
                    'date_published', 'publication_stage']
    list_filter = ['publication_stage', 'tags',
                   'date_published', 'date_last_edited']
    raw_id_fields = ('primary_media_object',)

    related_lookup_fields = {
        'fk': ['primary_media_object'],
    }    


    fieldsets = (
        (None, {
            'classes': ['wide',],    
            'fields': ('title', 'subtitle', 
                       ('date_published',  
                        'publication_stage'),
                        )
        }),
        (_('Primary image or video'),
        {
         'fields': ('primary_media_object',),
        }),
        (_('Content'),
         {'classes': ['editor',],
          'fields': ('blurb','text_format',),
        }),
        (_('How the story will be presented'),
         {'fields': ('display_editors','number_of_articles_per_page',
                     'contents_as_ordered_list')}
        ),
        (_('Categorise this story by giving it tags'),
         {'fields': ('tags',),
        }),        
        (_('Advanced options'), {
            'classes': ['collapse',],
            'fields': ( 'copyright',
                        'notes',
                       'users_who_can_edit_this', 
                       'slug',)
        }),
    )
    

class CreditAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_names', 'last_name', 'is_person',]
    list_editable =  ['first_names', 'last_name', 'is_person',]
    search_fields = ('first_names', 'last_name',)
    list_filter = ('is_person',)    

class OrderedArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'story', 'article', 'order',]
    list_editable = ['article', 'order']
    search_fields = ['story__title', 'article__title']
    list_filter = ['story', ]
    raw_id_fields = ('story', 'article',)
    related_lookup_fields = {
        'fk': ['story', 'article',],
    }    
    sortable_field_name = "order"      
    formfield_overrides = {
        IntegerField: {'widget': HiddenInput},
    }    
        

class FeaturedStoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'story', 'featured','order', ]
    list_editable = ['featured', 'order']
    search_fields = ['story__title', 'story__orderedarticle__article__title']
    raw_id_fields = ('story',)    
    related_lookup_fields = {
        'fk': ['story',],
    }    


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'submit_date', 'ip_address', 'is_public', 'is_removed']
    list_filter = ['is_public', 'is_removed']
    list_editable = ['is_public', 'is_removed']
    date_hierarchy = 'submit_date'    
    ordering = ['-submit_date']
    search_fields = ['^user__username', '^user__first_name', '^user__last_name','ip_address', 'comment']


class FeaturedWebpageGroupForm(forms.ModelForm):
    model = FeaturedWebpageGroup
    class Media:
        css = textarea_css
        js = jquery_js + textarea_js


class OrderedWebpageInline(admin.TabularInline):
    model = OrderedWebpage
    raw_id_fields = ['webpage',]
    sortable_field_name = "order"      
    formfield_overrides = {
        IntegerField: {'widget': HiddenInput},
    }    
    related_lookup_fields = {
        'fk': ['webpage',],
    }    



class FeaturedWebpageGroupAdmin(admin.ModelAdmin):
    form = FeaturedWebpageGroupForm 
    list_display = ['id', 'title', 'order', 'featured',]
    list_editable = ['featured',]
    list_filter = ['featured',]
    inlines = [OrderedWebpageInline,]


class FeaturedWebpageGroupLink(admin.ModelAdmin):
    raw_id_fields = ['media_object',]
    related_lookup_fields = {
        'fk': ['media_object',],
    }    


class WebpageLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', ]
    list_editable = ['title', 'url',]
    raw_id_fields = ['media_object',]
    related_lookup_fields = {
        'fk': ['media_object',],
    }    

    
    fieldsets = (
        (None, {    
            'fields': ('title', 'url',), 
        }),
        (_('Additional fields'),
         {
          'classes' : ['collapse',],
          'fields' : ('byline', 'date', 'html_A_tag_options', 'description',
                      'media_object'),
          }
         )
    )

class FeaturedRSSFeedAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'order', 'featured',]
    list_editable = ['featured',]
    list_filter = ['featured',]
    raw_id_fields = ['media_object']
    related_lookup_fields = {
        'fk': ['media_object',],
    }    


class FlatPageForm(forms.ModelForm):
    model = FlatPage
    class Media:
        js = [
              'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              'grappelli/tinymce_setup/tinymce_setup.js',
             ]
            
class CustomFlatPageAdmin(FlatPageAdmin):
    form = FlatPageForm  
      

class ImageAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ['id', '__unicode__', 'display', 'date_last_edited']
    raw_id_fields = ['captions',]
    related_lookup_fields = {
        'fk': ['captions',],
    }    

    
    formfield_overrides = {
        ImageField: {
            'form_class': ImageFormField,
            'widget': AdminImageWidget,
        }
    }
    
class FurtherReadingAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'url','category','order']
    list_editable = ['url', 'category', 'order',]
    raw_id_fields = ['article', 'url']
    related_lookup_fields = {
        'fk': ['article', 'url',],
    }    
    

class CaptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'language', 'text']     


admin.site.register(Copyright)
admin.site.register(MediaObject, MediaObjectAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(OutOfDate)
admin.site.register(HistoricalEdit)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(FurtherReading, FurtherReadingAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(OrderedArticle, OrderedArticleAdmin)
admin.site.register(FeaturedStory, FeaturedStoryAdmin)
admin.site.register(Credit, CreditAdmin)
admin.site.register(OrderedCredit)
admin.site.register(CommentFlag)
admin.site.register(UserProfile)
admin.site.register(Subscription)
admin.site.register(FeaturedWebpageGroup, FeaturedWebpageGroupAdmin)
admin.site.register(WebpageLink, WebpageLinkAdmin)
admin.site.register(OrderedWebpage)
admin.site.register(FeaturedRSSFeed, FeaturedRSSFeedAdmin)
admin.site.register(Video)
admin.site.register(Image, ImageAdmin)
admin.site.register(Caption, CaptionAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)


