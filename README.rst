THIS IS A WORK IN PROGRESS. PLEASE DO NOT FOLLOW THESE INSTRUCTIONS YET.

**************************
Django Publication Manager
**************************

Django Publication Manager, or Pubman for short, is a simple content management 
system built on Django. Its purpose is to provide you with a working website 
for your project from the start, freeing you to concentrate on implementing 
functionality specific to your project, without having to spend a large 
amount of time putting in the basic functionality that every website should 
have.

Another objective of Pubman is to provide your working website using free/open
source code only. For example, Pubman implements a search facility. Big search
companies like Google and Yahoo provide simple html snippets to do this, but 
since their search engines are not open, Pubman implements searching using 
Haystack_. Of course, you are welcome to not use the search facility.


Installing Pubman
=================

Pubman has been tested running Ubuntu 10.04, python 2.6 and 
Django 1.2.    

You can have a working Content Management System in Django by following these 
straightforward steps, each of which should take at most a few minutes of 
your time: 

#. Install the following
   
   - django-profiles_
   - sorl-thumbnail_
   - django-tagging_
   - django-registration_
   - django-contact-form_
   - glamkit-stopspam_
   - haystack_ and a search engine, e.g. Whoosh_ or Xapian_
   - django-treemenus_
   - django-siteconfig_  
   - django-filebrowser_ (Note this is a fork of the Grappelli dependent 
     version. It's quite possible other forked versions of django-filebrowser 
     will work too.)  
    

#. Install django-pubman using one of the standard python installation 
   mechanisms. E.g.   

   ::

    easy_install -Z pubman

#. In the folder pointed to by the MEDIA_URL setting in your project's 
   settings.py, either create a symbolic link called pubman to the 
   pubman/media/pubman folder or copy the contents of the pubman/media/pubman
   folder into the MEDIA_URL folder. 
       

#. Add the *django.middleware.locale.LocaleMiddleware* and
   *django.contrib.flatpages.middleware.FlatpageFallbackMiddleware* to 
   your MIDDLEWARE_CLASSES setting in settings.py. For example:
   
    :: 

    MIDDLEWARE_CLASSES = (              
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.locale.LocaleMiddleware',    
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.http.ConditionalGetMiddleware',
        'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',        
    )
    
#. In your project's settings.py put the following into INSTALLED_APPS if they 
   are not there already:

   ::

    ('django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.databrowse',   
    'django.contrib.comments',    
    'django.contrib.markup',    
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'filebrowser',
    'profiles',
    'sorl.thumbnail',    
    'tagging',
    'registration',
    'contact_form',
    'stopspam',
    'haystack',
    'treemenus',    
    'siteconfig',
    'pubman',)    

#. In your project's settings.py make sure the pubman templates folder is in 
   your TEMPLATE_DIRS tuple, but only after your project's templates, so that
   you can easily override pubman's templates. For example:

   ::

     TEMPLATE_DIRS = (os.path.join(SITE_ROOT, 'templates'),
                      os.path.join(SITE_ROOT, '/path_to_puman/pubman/templates'),)        
        
#. To make your website content searchable using Haystack, place this 
   into your project settings.py file:

   ::

    HAYSTACK_SITECONF = 'pubman.search_sites' 

   You will need to install a search engine such as *Whoosh* or *Xapian*. 
   In Ubuntu, for example, this is very easy: *apt-get --install whoosh* 
   should do the trick.  

   Once you have done so, add this to your settings.py file.

   ::

    HAYSTACK_SEARCH_ENGINE =  'whoosh'
    HAYSTACK_WHOOSH_PATH = 'whoosh'

   or if you are using Xapian
   
   ::
    
    HAYSTACK_SITECONF = 'pubman.search_sites'
    HAYSTACK_SEARCH_ENGINE = 'xapian'
    HAYSTACK_XAPIAN_PATH = os.path.join(SITE_ROOT, 'xapian')
    
   More details are available in the Haystack documentation, including how to
   install different search engines.,
   
   Of course, you could simply use a site like google or yahoo for your searching,
   but one of the aims of pubman is to provide a comprehensive set of free/open 
   source website widgets.

#. Then install the pubman tables and initial data:
   
   :: 

    python manage.py syncdb   
   

#. You can upload other data to your database as well. Data fixtures (initial 
   data) are provided for the flatpages, sites, auth and treemenus apps. If 
   this is a new project, then you will almost certainly want to run the following:
   
   ::
    python manage.py loaddata sites website treemenus flatpages 
   
   However, if you are introducing pubman into an existing project, running the 
   above might wipe out some of your existing data, so be careful. For example,
   the sites fixture replaces your first site (pk=1) with a domain of *localhost:8000* 
   and a name of *Publication Manager*. This is probably not very useful, but it is 
   arguably slightly more useful than the Django default of *example.com*.

   You can choose to upload any or none of the above. But note that Publication Manager
   expects a top level menu to exist called "main". If you do not provide one, a template 
   exception will be thrown when you go to the front page of your website. So it 
   is very likely you will want to load the treemenus fixture. To install just the 
   treemenus data, run:
   
   ::
    
    python manage.py loaddata treemenus
    


   At this point you should have a basic working configuration. If you run 
   the Django development server, you should be able to go to 
   http://localhost:8000/

#. To get authorisation, authentication and user profiles working put 
   this into your project's settings.py:

   ::
   
    ACCOUNT_ACTIVATION_DAYS = 2 # This is 2 days. You can change this.
    LOGIN_REDIRECT_URL = '/' # This is a default. You can change this.
    AUTHENTICATION_BACKENDS = (
        'pubman.accounts.backends.EmailOrUsernameModelBackend',
        'django.contrib.auth.backends.ModelBackend'
    )
    AUTH_PROFILE_MODULE = 'pubman.UserProfile'

   This enables email confirmed registration and allows users to login with 
   their email address or username.  

#. Pubman's views and default templates use Django's caching framework. In 
   production this is indispensable for decent performance. Enable the Django
   caching_ framework.   
   To enable caching on in production, but not while developing,
   this is what you could put into your project's settings.py file:

   ::

    if DEBUG==True:
        CACHE_BACKEND = 'dummy://'    
    else:     
        CACHE_BACKEND = 'memcached://www.example.com:11211/'

   Replace *www.example.com* with your website's URL, of course.

#. Enable the pubman urls. In the project's urls.py file add this to the 
   urlpatterns tuple (you can of course customise this to your needs):

   ::

    (r'^', include('pubman.urls')),

#. Enable the pubman template context processors. These are 
   *pubman.context_processors.settings* and 
   *pubman.context_processors.featured_content*. For example, you would usually
   add this to the settings.py file:  

   ::
   
    TEMPLATE_CONTEXT_PROCESSORS = (
       "django.contrib.auth.context_processors.auth",
       "django.core.context_processors.debug",
       "django.core.context_processors.i18n",
       "django.core.context_processors.media",
       "django.core.context_processors.request",    
       "django.contrib.messages.context_processors.messages",
       "pubman.context_processors.settings",
       "pubman.context_processors.featured_content",
       "siteconfig.context_processors.rootdivision",    ) 

#. Get the Filebrowser to work by putting these settings into settings.py:

   ::
   
    import os 
    FILEBROWSER_DIRECTORY = 'userfiles/uploads/'
    FILEBROWSER_URL_FILEBROWSER_MEDIA = MEDIA_URL + 'pubman/filebrowser/'
    FILEBROWSER_PATH_FILEBROWSER_MEDIA = os.path.join(MEDIA_ROOT, 'pubman/filebrowser/')
    FILEBROWSER_URL_TINYMCE = MEDIA_URL + "pubman/js/tiny_mce/"
    FILEBROWSER_PATH_TINYMCE = os.path.join(MEDIA_ROOT, 'pubman/js/tiny_mce/')
    
    
At this point your pubman configuration should be configured and all features 
enabled.  


Current Features
================

Pubman currently implements the following:

- Upon successful standard installation you will have an operating website.
- A Content Management System that allows you to add content via Django's admin 
  site. It has several nice features which are described under CMS features_.     
- A comprehensive base.html template and style sheet.
- RSS and Atom feeds for the website.
- Language switching views and templates using Django's i18n features.
- Account registration, login using email address or username, user profile
  views and templates and user lost password authentication (using 
  django-registration_ and django-profiles_).    
- A simple contact form (using django-contact-form_) 
- A simple sitemap.
- Careful attention to caching at both view and template level.
- Hierarchical menus can be created and deleted in database (using django-treemenus_).  

.. _features:

CMS features
------------

Pubman is primarily a CMS. Content is created via Django's admin interface. 
It currently has the following features:

- A workflow for creating website articles from draft to publication.
- Articles can be grouped into stories.
- Articles and stories can have teasers, which in Pubman are called blurbs.  
- Management of media. Currenly only photos on the site are implemented, but
  video and media offsite are a priority for the next version.
- Tags and Tag clouds for Articles, including a view that processes complex tag
  expressions (using django-tagging_).
- Manages translations of articles, presenting them seamlessly to users.
- Links to related articles and stories are easily incorporated into articles.
- Groups sets of links for easy presentation.
- Simple feed reader.
- Manages copyrights.
- Articles, stories and translations can be written in plain text, Markdown 
  or HTML. Users Markdown or TinyMCE editors for Markdown or HTML respectively.   
- Filebrowser implemented on Django admin interface and integrated into TinyMCE
  (using a forked version of django-filebrowser_).  

Planned future features
-----------------------

- Attach documents to articles
- Improved contact form with more options.
- PDF generation of articles and stories.
- Newsletter
- User blogs
- Media objects other than local images
- Style sheet for mobile devices
- See historical edits
- Improved foreign key lookup with AJAX
- Specify an article as out-of-date with links to recommended replacement
  article.
        
.. _Haystack: http://haystacksearch.org


.. _caching: http://docs.djangoproject.com/en/1.2/topics/cache/
.. _django-profiles: https://bitbucket.org/ubernostrum/django-profiles
.. _sorl-thumbnail: https://github.com/sorl/sorl-thumbnail
.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/
.. _django-contact-form: https://bitbucket.org/ubernostrum/django-contact-form/
.. _django-treemenus: https://github.com/jphalip/django-treemenus
.. _django-tagging: http://code.google.com/p/django-tagging/
.. _django-filebrowser: https://github.com/jbeaurain/django-filebrowser-no-grappelli
.. _whoosh: http://whoosh.ca/
.. _xapian: http://xapian.org/
.. _django-siteconfig: https://launchpad.net/django-siteconfig
.. _glamkit-stopspam: https://github.com/glamkit/glamkit-stopspam
