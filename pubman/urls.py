'''URLconf for pubman

These are:
    /    Index of articles page. Good for a homepage.
    /mediaobject/*
    /article/*
    /story/* 
    /copyright/*
    /feed/rss/
    /feed/atom/
    /i18n/*
    /accounts/*
    /comments/*
    /contact/
    /profiles/*
    /sitemap.xml
'''

from django.conf.urls.defaults import *
from pubman import settings

from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template

from pubman.views import media_object_detail, search
from pubman.models import Story, Copyright
from pubman.feeds import LatestArticlesRSSFeed, LatestArticlesAtomFeed

from django.contrib.sitemaps import FlatPageSitemap
from contact_form.views import contact_form

from pubman.sitemap import ArticleSitemap, StorySitemap, TranslationSitemap 
from pubman.forms import PubmanContactForm

import datetime

story_info = {
    "queryset" : Story.objects.filter(publication_stage='P').\
        filter(date_published__lte = datetime.datetime.now()).\
        order_by('-date_published'),
    "paginate_by" : settings.STORIES_PER_PAGE, 
}

copyright_info = {
    "queryset" : Copyright.objects.all(),
}


sitemaps = {
    'flatpages': FlatPageSitemap,
    'article': ArticleSitemap,
    'story': StorySitemap, 
    'translation': TranslationSitemap,
}


urlpatterns = patterns('pubman.views',
    (r'^$', 'index'),
    url(r'^mediaobject/(?P<slug>[a-zA-Z0-9-\s_]+)/$', 
     media_object_detail,
     name='media_object_detail_view'),
    
    (r'^article/(?P<article_id>\d+)/$', 'article_detail_by_id'),
    url(r'^article/(?P<article_slug>[a-zA-Z0-9-_]+)/$', 
        'article_detail', name='article_detail_view'),    
    
    url(r'^article/translation/(?P<article_slug>[a-zA-Z0-9-_]+)/(?P<article_lang>[a-zA-Z0-9-_]+)/$', 
        'article_detail', name='translated_article'),    

    (r'^article/tag/(?P<tag_expression>[\"\^\'\~\&\|\(\)a-zA-Z0-9-\s_]+)/$', 'tag_view', 
     {'model_name': 'article', }, 
    'article_tag'),

    (r'^story/$', list_detail.object_list, story_info),
    (r'^story/(?P<story_id>\d+)/$', 'story_detail_by_id'),
    (r'^story/(?P<story_slug>[a-zA-Z0-9-_]+)/$', 'story_detail'),
    url(r'^copyright/(?P<object_id>\d+)/$', 
        list_detail.object_detail, 
        copyright_info,
        name='copyright_view'),
    
    (r'^markdownpreview/$', 'markdownpreview'),
    (r'^clearcache/$', 'clear_cache')
)

if 'search' in settings.URLCONF_VIEWS:
    urlpatterns += patterns(settings.URLCONF_ROOT,
                        (r'^search/$', search),)

if 'rss' in settings.URLCONF_VIEWS: 
    urlpatterns += patterns(settings.URLCONF_ROOT,
            url(r'^feed/rss/articles/$', LatestArticlesRSSFeed(), name='rss-feed-articles'),)
    
if 'atom' in settings.URLCONF_VIEWS:
    urlpatterns += patterns(settings.URLCONF_ROOT,                
            url(r'^feed/atom/articles/$', LatestArticlesAtomFeed(), name='atom-feed-articles'),)

if 'i18n' in settings.URLCONF_VIEWS:
    urlpatterns += patterns(settings.URLCONF_ROOT,         
            url(r'^i18n/setlangform/', direct_to_template,
            {'template': 'pubman/set_language.html'}, name='setlangform' ),  
            (r'^i18n/', include('django.conf.urls.i18n')),)

if 'accounts' in settings.URLCONF_VIEWS:
    urlpatterns += patterns(settings.URLCONF_ROOT,    
            (r'^accounts/', include('registration.urls')),)

if 'comments' in settings.URLCONF_VIEWS:
    urlpatterns += patterns(settings.URLCONF_ROOT,    
            (r'^comments/', include('django.contrib.comments.urls')),)

if 'contact' in settings.URLCONF_VIEWS:
    urlpatterns += patterns(settings.URLCONF_ROOT,
            
    (r'^contact/$', contact_form, {'form_class': PubmanContactForm}),                            
    (r'^contact/', include('contact_form.urls')),)
    
if 'profiles' in  settings.URLCONF_VIEWS:
    urlpatterns += patterns(settings.URLCONF_ROOT,
            (r'^profiles/create/$', 'pubman.views.edit_profile'),
            (r'^profiles/edit/$', 'pubman.views.edit_profile'),
            (r'^profiles/', include('profiles.urls')),)
    
if 'sitemap' in settings.URLCONF_VIEWS:
    urlpatterns += patterns(settings.URLCONF_ROOT,
    (r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),)        

if 'filebrowser' in settings.URLCONF_VIEWS:
    urlpatterns += patterns(settings.URLCONF_ROOT,
    (r'^admin/filebrowser/', include('filebrowser.urls')),)