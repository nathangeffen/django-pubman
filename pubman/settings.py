import os

from django.conf import settings
from django.utils.translation import ugettext as _
from pubman.utils import set_additional_languages

PUBMAN_VERSION = "0.5beta"

MAX_CHAR_FIELD_LENGTH = getattr(settings,'PUBMAN_MAX_CHAR_FIELD_LENGTH', 200)
ARTICLES_PER_PAGE = getattr(settings,'PUBMAN_ARTICLES_PER_PAGE', 10)
STORIES_PER_PAGE = getattr(settings,'PUBMAN_STORIES_PER_PAGE', ARTICLES_PER_PAGE)

UPLOAD_IMAGES_FOLDER_MASK = getattr(settings,
    'PUBMAN_UPLOAD_IMAGES_FOLDER_MASK', 'userfiles/uploads/images/%Y/%m/%d')

UPLOAD_AVATAR_FOLDER_MASK = getattr(settings,
    'PUBMAN_UPLOAD_AVATAR_FOLDER_MASK', 'userfiles/uploads/images/avatars')

UPLOAD_VIDEOS_FOLDER_MASK = getattr(settings,
    'PUBMAN_UPLOAD_VIDEOS_FOLDER_MASK', 'userfiles/uploads/videos/%Y/%m/%d')

DEFAULT_IMAGE_WIDTH = getattr(settings, 'PUBMAN_DEFAULT_IMAGE_WIDTH', 500)
DEFAULT_IMAGE_HEIGHT = getattr(settings, 'PUBMAN_DEFAULT_IMAGE_HEIGHT', 500)

DEFAULT_THUMB_IMAGE_WIDTH = getattr(settings, 'PUBMAN_DEFAULT_IMAGE_WIDTH', 50)
DEFAULT_THUMB_IMAGE_HEIGHT = getattr(settings, 'PUBMAN_DEFAULT_IMAGE_HEIGHT', 50)

DEFAULT_PASSPORT_IMAGE_WIDTH = getattr(settings, 'PUBMAN_PASSPORT_IMAGE_WIDTH', 150)
DEFAULT_PASSPORT_IMAGE_HEIGHT = getattr(settings, 'PUBMAN_PASSPORT_IMAGE_HEIGHT', 150)

DEFAULT_TEXT_FORMAT = getattr(settings, 'PUBMAN_DEFAULT_TEXT_FORMAT', 'H')

TEMPLATE_DIRS = getattr(settings, 'TEMPLATE_DIRS') +\
    (os.path.join(os.path.dirname(os.path.realpath(__file__)),
    'templates/pubman'),
    )


PAGE_BREAK_CODE = getattr(settings, 'PUBMAN_BREAK_CODE', '<!--pagebreak-->')
PAGE_BREAK_WORD_COUNT = getattr(settings, 'PUBMAN_BREAK_WORD_COUNT', 800)
PAGE_BREAK_PARA_COUNT = getattr(settings, 'PUBMAN_PARA_COUNT', 8)

TEXT_SHORTEN_CODE = getattr(settings, 'PUBMAN_TEXT_SHORTEN_CODE', '<!--shorten-->')

COMMENTERS_MUST_BE_AUTHENTICATED = getattr(settings, 'PUBMAN_COMMENTERS_MUST_BE_AUTHENTICATED', False)

COMMENTS_MODERATED = getattr(settings, 'PUBMAN_COMMENTS_MODERATED', False)
MODERATION_FREE_DAYS = getattr(settings, 'PUBMAN_MODERATION_FREE_DAYS', -1)
CLOSE_AFTER_DAYS = getattr(settings, 'PUBMAN_CLOSE_AFTER', 14)

EMAIL_COMMENTS_TO_STAFF = getattr(settings, 'PUBMAN_EMAIL_COMMENTS_TO_STAFF', False)

NUMBER_AUTHORS_TO_PRINT = getattr(settings, 'PUBMAN_NUMBER_AUTHORS_TO_PRINT', 2)

OTHER_AUTHORS_TEXT = getattr(settings, 'PUBMAN_OTHER_AUTHORS_TEXT', 'et al.')

ISHARE = getattr(settings, 'PUBMAN_ISHARE', True)

PRINT_THIS = getattr(settings, 'PUBMAN_PRINT_THIS', True)

CACHE_PERIOD = getattr(settings, 'PUBMAN_CACHE_PERIOD', 900)

FEED_CACHE_PERIOD = getattr(settings, 'PUBMAN_FEED_CACHE_PERIOD', 7200)

FEED_TITLE = getattr(settings, 'PUBMAN_FEED_TITLE', u'Publication Manager')

FEED_DESCRIPTION = getattr(settings, 'PUBMAN_FEED_DESCRIPTION',
                           u'Latest articles')

FEED_ICON_URL = getattr(settings, 'PUBMAN_FEED_ICON_URL', '/feed/rss/articles')

DEFAULT_RSS_READER_ITEMS = getattr(settings, 'PUBMAN_DEFAULT_RSS_READER_ITEMS', 5)

NUM_COMMENTS_ON_ARTICLES = getattr(settings, 'PUBMAN_NUM_COMMENTS_ON_ARTICLE', True)

MARKDOWN_EXTENSIONS = getattr(settings, 'PUBMAN_MARKDOWN_EXTENSIONS',
                              'abbr,tables,def_list,footnotes')

ugettext = lambda s: s

ADDITIONAL_LANGUAGES = getattr(settings, 'PUBMAN_ADDITIONAL_LANGUAGES',(
            ('af', ugettext(u'Afrikaans')),
            ('nr', ugettext(u'S. Ndebele')),
            ('ss-ZA', ugettext(u'Swati')),
            ('tn-ZA', ugettext(u'Tswana')),
            ('ts', ugettext(u'Tsonga')),
            ('ve', ugettext(u'Venda')),
            ('xh', ugettext(u'Xhosa')),
            ('zu', ugettext(u'Zulu')),))

ALL_LANGUAGES = set_additional_languages(getattr(settings, 'LANGUAGES'),
                                                ADDITIONAL_LANGUAGES,)

try:
    DEFAULT_LANGUAGE_INDEX = [i[0] for i in ALL_LANGUAGES].index(settings.LANGUAGE_CODE)
except ValueError:
    try:
        DEFAULT_LANGUAGE_INDEX = [i[0] for i in ALL_LANGUAGES].index(settings.LANGUAGE_CODE[0:2])
    except:
        DEFAULT_LANGUAGE_INDEX = 1

URLCONF_ROOT = getattr(settings, 'PUBMAN_URLCONF_ROOT','')

URLCONF_VIEWS = getattr(settings, 'PUBMAN_URLCONF_VIEWS',
                   ('search',
                   'rss',
                   'atom',
                   'i18n',
                   'accounts',
                   'comments',
                   'contact',
                   'profiles',
                   'sitemap',
                   'filebrowser',))

SITE_ID = getattr(settings, 'SITE_ID', 1)

TEMPLATE_SETTINGS = getattr(settings,'PUBMAN_TEMPLATE_SETTINGS',
                            ['SITE_ID',
                             'DEFAULT_IMAGE_WIDTH',
                             'DEFAULT_IMAGE_HEIGHT',
                             'DEFAULT_THUMB_IMAGE_WIDTH',
                             'DEFAULT_THUMB_IMAGE_HEIGHT',
                             'DEFAULT_PASSPORT_IMAGE_WIDTH',
                             'DEFAULT_PASSPORT_IMAGE_HEIGHT',
                             'ISHARE',
                             'NUM_COMMENTS_ON_ARTICLES',
                             'FEED_ICON_URL',
                             'FEED_CACHE_PERIOD',
                             'CACHE_PERIOD', ])

