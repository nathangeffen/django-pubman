'''Context processors that return queries for featured content as well as some 
settings used in templates. 

Functions:
    
    settings: returns settings specified in PUBMAN_TEMPLATE_SETTINGS (which is 
        just TEMPLATE_SETTINGS by the time this processor is called.)
    
    featured_content: returns queries to featured_content 
     
'''


from pubman import settings as s
from django.contrib.sites.models import Site
from pubman.models import FeaturedStory
from pubman.models import FeaturedWebpageGroup
from pubman.models import FeaturedRSSFeed


def settings(request):
    '''Puts settings specified in TEMPLATE_SETTINGS (or PUBMAN_TEMPLATE_SETTINGS 
    from the perspective of a user of pubman) into the template context.
    '''

    setting_dict = { 'settings' : {
        }
    }
    
    if s.TEMPLATE_SETTINGS:
        for setting in s.TEMPLATE_SETTINGS:
            setting_dict['settings'][setting] =\
                getattr(s, setting, None)

    if 'SITE_ID' in setting_dict['settings']:
        setting_dict['settings']['SITE_NAME'] =\
            Site.objects.get_current().name
            
    if 'DEFAULT_IMAGE_WIDTH' in setting_dict['settings'] and\
        'DEFAULT_IMAGE_HEIGHT' in setting_dict['settings']:
        setting_dict['settings']['DEFAULT_IMAGE_DIM'] =\
            unicode(setting_dict['settings']['DEFAULT_IMAGE_WIDTH']) +\
            u'x' + unicode(setting_dict['settings']['DEFAULT_IMAGE_HEIGHT'])
            
    if 'DEFAULT_THUMB_WIDTH' in setting_dict['settings'] and\
        'DEFAULT_THUMB_HEIGHT' in setting_dict['settings']:
        setting_dict['settings']['DEFAULT_THUMB_DIM'] =\
            unicode(setting_dict['settings']['DEFAULT_THUMB_WIDTH']) +\
            u'x' + unicode(setting_dict['settings']['DEFAULT_THUMB_HEIGHT'])

    if 'DEFAULT_THUMB_IMAGE_WIDTH' in setting_dict['settings'] and\
        'DEFAULT_THUMB_IMAGE_HEIGHT' in setting_dict['settings']:
        setting_dict['settings']['DEFAULT_THUMB_DIM'] =\
            unicode(setting_dict['settings']['DEFAULT_THUMB_IMAGE_WIDTH']) +\
            u'x' + unicode(setting_dict['settings']['DEFAULT_THUMB_IMAGE_HEIGHT'])

    if 'DEFAULT_PASSPORT_IMAGE_WIDTH' in setting_dict['settings'] and\
        'DEFAULT_PASSPORT_IMAGE_HEIGHT' in setting_dict['settings']:
        setting_dict['settings']['DEFAULT_PASSPORT_DIM'] =\
            unicode(setting_dict['settings']['DEFAULT_PASSPORT_IMAGE_WIDTH']) +\
            u'x' + unicode(setting_dict['settings']['DEFAULT_PASSPORT_IMAGE_HEIGHT'])

    if request.user.is_authenticated() and request.user.has_perm('pubman.add_article'):
        setting_dict['settings']['CAN_ADD_ARTICLE'] = True
    else:
        setting_dict['settings']['CAN_ADD_ARTICLE'] = False

    return setting_dict


def featured_content(request):
    '''Returns a dictionary of queries for featured content.
    '''
    featured_content_dict = {}
    
    featured_content_dict['featured_webpage_groups'] = FeaturedWebpageGroup.objects.filter(featured=True)
    featured_content_dict['featured_feeds'] = FeaturedRSSFeed.objects.filter(featured=True)    
    featured_content_dict['featured_stories'] = FeaturedStory.objects.filter(FeaturedStory.is_featured_Q())

    return featured_content_dict
