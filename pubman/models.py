"""Models for handling publication content in Publication Manager.

Models:

    UserProfile: Extension to django's User model.

    Subscription: Tracks subscriptions to this publication's articles.
        Not fully implemented yet. Low priority given that I'm not much
        interested in this feature.

    Copyright: These are foreign keys in all models inheriting from ContentObject
    and represent the different types of copyrights that this publication's
    materials can be published under.

    Credit: Model representing people or institutions who are photographers,
    writers editors etc.

    OrderedCredit: Used to order authors/credits for content models
        (articles, media objects, stories and translations).

    ContentObject: Abstract base class that Article, Story, MediaObject and
        Translation inherit from.

    MediaObject: Represents images, video etc. Needs a lot more work.

    Article: Stores article items. This is the central model in pubman around
        which most of the other models work.

    OutOfDate: Reserved for future use to represent articles that are out of
        date and have been superceded.

    HistoricalEdit: Reserved for future use to represent modifications to
        articles, a bit like a Wiki.

    Translation: Model whose instances are a translation of an article.

    FurtherReading: Each instance is a link to a recommended further reading
        for an article. These recommended readings can be other articles,
        stories or external URLs.

    Story: Each instance contains a collection of articles. Nice for featuring
        a set of related articles or creating tutorials.

    OrderedArticle: Model used to order an article within a story.

    FeaturedStory: OneToOne with Story that is used to indicate what stories
        should be featured, e.g. on the front page of the website.

    FeaturedWebpageGroup: Model for representing a collection of links to
        external sites. E.g. for representing links, perhaps blogrolls etc.

    WebpageLink: Each instance represents link to external URL. There are many
        of these in each FeaturedWebPageGroup via WebPageOrder.

    OrderedWebpage: Used to order the WebPageLinks within a FeaturedWebPageGroup.

    FeaturedRSSFeed: Extremely simple model for keeping external feeds that the
        website must get.

"""

from django.db import models
from django.db.models import Q
from datetime import datetime, timedelta

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings as django_settings

import feedparser

from django_countries import CountryField
from sorl.thumbnail import ImageField, get_thumbnail
from tagging.fields import TagField

from pubman.settings import MAX_CHAR_FIELD_LENGTH as MAX_LENGTH
from pubman.settings import ALL_LANGUAGES, DEFAULT_LANGUAGE_INDEX
from pubman import settings
from pubman.utils import set_extra_permissions, is_published, make_slug_unique,\
    permission_to_view_Q, permission_to_view_item, credit_list, validate_link,\
    get_link, get_caption


# "Monkey patch" the username field to be 75 chars long so that
# emails can be entered in authentication username field.
AuthenticationForm.base_fields['username'].max_length = 75

users_who_can_edit_this_help_text = _("Indicate which users can edit or delete " +\
                    "this content. ")

slug_field_help_text = _('This is the name of the item in its URL. ' +\
                       'It is automatically created from the title. ' +\
                       'If you do edit it, it may only contain letters, ' +\
                       'digits, hyphens and underscores. ' +\
                       'The slug must be unique. ')

publication_stage_help_text = _('This item only becomes available to site users '
        'when you change this to published and the publication date has been reached. ')

COMPLEXITY_CHOICES = (
    ('S', _('simple')),
    ('D', _('difficult'))
)

PUBLICATION_STAGES = (
    # ('W', _('withdrawn')),
    ('D', _('draft')),
    # ('S', _('submitted')),
    ('P', _('published')),
)

MEDIA_TYPES = (
    ('I', _('Photos or Images on this site')),
    ('V',_('Video on this site')),
    ('E', _('Embedded image, map or video from another site')),
)

TYPES_OF_FURTHER_READING = (
    ('00', _('Related articles')),
    ('05', _('Further Reading')),
    ('10', _('See also')),
    ('15', _('Source')),
    ('20', _('Reference'))
)

TEXT_FORMATS = (
    ('T', _('Plain text')),
    ('R', _('reStructuredText')),
    ('M', _('Markdown')),
    ('H', _('HTML')),
)

PAGE_BREAK_STRATEGIES = (
    ('N', _('No breaks')),
    ('C', _('Break when encountering this: ' +\
             settings.PAGE_BREAK_CODE)),
    )

EDITOR_DISPLAY_STYLES = (
    ('N', _('Do not display editors')),
    ('E', _('Display as editors')),
    ('A', _('Display as authors')),
    )

SEXES= (('F',_('Female')),
        ('M', _('Male'),))

VIDEO_LOAD_CHOICES = (
        ('A', _('Autoplay')),
        ('D', _('Default')),
        ('N', _('Do not preload')),
        ('P', _('Do preload')),
    )

# Constants used by MediaObject class to determine if HTML for a slideshow
# must be generated.
SLIDESHOW = -1
ALL_IMAGES = -2


class UserProfile(models.Model):
    '''Extension to Django's User model
    '''
    user = models.OneToOneField(User)
    avatar = ImageField(upload_to=settings.UPLOAD_AVATAR_FOLDER_MASK,
                        blank=True,
                        verbose_name='Photo or avatar')
    date_of_birth = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True, verify_exists=False,
                          verbose_name='Your website')
    sex = models.CharField(max_length=1,
                           choices=SEXES, blank=True, null=True)
    physical_address = models.CharField(max_length=MAX_LENGTH,
                            blank=True)
    physical_address_code = models.CharField(max_length=12,
                            blank=True)
    physical_address_city = models.CharField(max_length=MAX_LENGTH,
                            blank=True)
    physical_address_country = CountryField(blank=True)
    postal_address = models.CharField(max_length=MAX_LENGTH,
                            blank=True)
    postal_address_code = models.CharField(max_length=12,
                            blank=True)
    postal_address_city = models.CharField(max_length=MAX_LENGTH,
                            blank=True)
    postal_address_country = CountryField(blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

class Subscription(models.Model):
    '''Tracks subscriptions to the publication's articles. Not fully implemented
    yet.
    '''
    subscriber = models.ForeignKey(UserProfile)
    date_from = models.DateField()
    date_to = models.DateField()

    @staticmethod
    def is_subscriber(user):
        if Subscription.objects.filter(user__id=user.id,
                                date_from__lt=datetime.today(),
                                date_to__gt=datetime.today()).count()>0:
            return True
        else:
            return False

    class Meta:
        verbose_name = _('subscriber')
        verbose_name_plural = _('subscribers')


class Copyright(models.Model):
    """This class represents the different types of copyrights that
    can be applied to an image or article.
    """
    title = models.CharField(max_length=MAX_LENGTH)
    easy_text = models.TextField(blank=True,
        help_text=_('Explanation of copyright for non-experts.'))
    legal_text = models.TextField(blank=True,
        help_text = _('Actual legal text of the copyright.'))
    html_text = models.TextField(blank=True,
        help_text = _('HTML that can be placed on web pages '
                      'of objects under this copyright. '))
    url = models.URLField(blank=True,
        verify_exists=False,
        help_text=_('Web address for this copyright.'))

    def describe(self):
        return self.easy_text

    @models.permalink
    def get_absolute_url(self):
        return ('copyright_view', [str(self.id)])

    def get_name(self):
        return self._meta.verbose_name

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('copyright')
        verbose_name_plural = _('copyrights')

class Credit(models.Model):
    """Model representing people or institutions who are photographers,
    writers editors etc.
    """
    is_person = models.BooleanField(default=True,
                                 verbose_name='Is this a person?',
                                 help_text=_('Check this field if this is a '
                                 'person (e.g. Thomas Hardy) as opposed to '
                                 'an institution (e.g. Reuters).'))
    first_names = models.CharField(blank=True, max_length=MAX_LENGTH,
                                  verbose_name=_("Person's first names"),
                                  help_text=_('Leave blank for institutions'))
    last_name = models.CharField(max_length=MAX_LENGTH,
                                 verbose_name=_('Name of institution or '
                                 'last name of person'))
    tags = TagField(help_text=_('Comma separated list of tags. '
                                'E.g. "Pullitzer prize winner", '
                                '"foreign language specialist" etc. '
                                'Each tag must start with a letter and can contain '
                                'letters, digits, spaces and underscores.'))

    def __unicode__(self):
        if self.is_person and unicode(self.first_names).strip():
            return self.first_names + ' ' + self.last_name
        else:
            return self.last_name

    def title(self):
        return self.__unicode__()

    def detail(self):
        if self.is_person:
            return _("Some content on this site is credited to this person.")
        else:
            return _("Some content on this site is credited to this institution.")

    class Meta:
        verbose_name = _('credit (author etc.)')
        verbose_name_plural = _('credits (authors etc.)')

class OrderedCredit(models.Model):
    """Model for ordered authors or credits for an article or media object.

    This class is necessary to specify whether an author or credit is first
    author, second authors etc.
    """
    author_or_institution = models.ForeignKey(Credit)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    order = models.IntegerField(blank = True,
                                null = True,
                                default = 0,
                                help_text=_('Enter a number indicating '\
                                'first author, second author etc.'))

    def __unicode__(self):
        return self.author_or_institution.__unicode__()

    class Meta:
        verbose_name = 'Author, creator or credit'
        verbose_name_plural = 'Authors, creators or credits'
        ordering = ['order',]
        unique_together = ('content_type', 'object_id', 'author_or_institution')

class ContentObject(models.Model):
    '''Abstract base class for models representing content and that have many
    of the same  fields.
    '''
    title = models.CharField(max_length=MAX_LENGTH)
    subtitle = models.CharField(max_length=MAX_LENGTH, blank=True)
    date_published = models.DateTimeField(blank=True, null=True, default=datetime.now)
    publication_stage = models.CharField(max_length=1,
        choices = PUBLICATION_STAGES, default='D',
        help_text=publication_stage_help_text)
    slug = models.SlugField(max_length=MAX_LENGTH,
                            unique=True,
                            help_text=slug_field_help_text,)
    copyright = models.ForeignKey(Copyright, blank=True, null=True, default=2)
    date_last_edited = models.DateTimeField(auto_now=True, editable=False)
    notes = models.TextField(blank=True)
    tags = TagField(help_text=_('Comma separated list of tags.'))
    author = generic.GenericRelation(OrderedCredit, verbose_name='Credit')
    users_who_can_edit_this = models.ManyToManyField(User,
        blank=True,
        null=True,
        help_text=users_who_can_edit_this_help_text)

    def is_published(self):
        return is_published(self)

    def save(self, *args, **kwargs):
        make_slug_unique(self)
        super(ContentObject, self).save(*args, **kwargs)

    def permission_to_view_item(self, user):
        return permission_to_view_item(self, user)

    def authors_et_al(self, number_to_print=settings.NUMBER_AUTHORS_TO_PRINT):
        return credit_list(self.author, number_to_print)

    def full_author_list(self):
        return self.authors_et_al(0)

    def publish(self, immediately=False):
        self.publication_stage = 'P'
        if not self.date_published:
            self.date_published = datetime.now()
        if immediately and self.date_published > datetime.now():
            self.date_published = datetime.now()
        self.save()

    class Meta:
        abstract = True

class Video(models.Model):
    title = models.CharField(max_length=MAX_LENGTH)
    video_file = models.FileField(upload_to=settings.UPLOAD_VIDEOS_FOLDER_MASK)
    html_type_attribute = models.CharField(max_length=MAX_LENGTH,
                blank=True,
                help_text=_('This is the HTML5 type attribute for videos. '
                            'Safe to leave blank. For advanced use only.'))

class Caption(models.Model):
    text = models.CharField(max_length=MAX_LENGTH)
    language = models.CharField(max_length=7,
                                choices=ALL_LANGUAGES,
                                default=ALL_LANGUAGES[DEFAULT_LANGUAGE_INDEX][0])
    date_last_edited = models.DateTimeField(editable=False, auto_now=True)

    def __unicode__(self):
        return unicode(self.language) + u': ' + self.text

    class Meta:
        ordering = ['-date_last_edited']

class Image(models.Model):
    image =  models.ImageField(upload_to=settings.UPLOAD_IMAGES_FOLDER_MASK)
    captions = models.ManyToManyField(Caption, blank=True, null=True,
            help_text=_('Captions for this specific image. Use only '
                        'one caption per language.'))
    date_last_edited = models.DateTimeField(editable=False, auto_now=True)

    def display(self, width=settings.DEFAULT_THUMB_IMAGE_WIDTH,
                    height=settings.DEFAULT_THUMB_IMAGE_HEIGHT):
        im = get_thumbnail(self.image, unicode(width)+'x'+unicode(height),
                           crop='center', quality=99)
        output = '<img src="' + im.url + '" ' + 'width=' + unicode(width) + ' height=' +\
            unicode(height) + '\>'
        return output

    display.allow_tags = True
    display.admin_order_field = 'date_last_edited'

    def get_caption(self,
                    language=settings.ALL_LANGUAGES[settings.DEFAULT_LANGUAGE_INDEX][0]):
        return get_caption(self, language)

    def __unicode__(self):
        return self.image.url

    class Meta:
        ordering = ['-date_last_edited']



class MediaObject(ContentObject):
    """Model for representing images used in articles of all publications.

    Articles contain text which refer to images and other media,
    some of which will be stored on the server and represented by this model.
    """

    media_type = models.CharField(max_length=2, choices=MEDIA_TYPES, default='I')
    images = models.ManyToManyField(Image, blank=True, null=True,
            help_text=_('For images on this site. '
                    'If more than one image is used, they will display as a '
                    'slideshow.'))
    video_files = models.ManyToManyField(Video, blank=True, null=True,
        help_text=_('For videos on this site. This uses HTML 5 which is not '
                    'supported by older browsers and often only partly '
                    'supported on newer ones. '
                    'This option is complicated and recommended for '
                    'advanced users only. '
                    'A simpler (albeit not entirely satisfactory) alternative '
                    'is to use an embedded video from '
                    'an external website.'))
    preload = models.CharField(max_length=2, choices=VIDEO_LOAD_CHOICES,
                default='D',
                help_text=_('Indicates if the video loads as soon as the page '
                            'is downloaded.'))
    embedded = models.TextField(blank=True,
        help_text=_('For video, images, maps or sound on other sites.'))
    captions = models.ManyToManyField(Caption, blank=True, null=True,
        help_text=_('Caption that is displayed for this entire media object. '
                    'One per language. '))
    date_captured = models.DateTimeField(blank=True, null=True)

    @staticmethod
    def permission_to_view_Q(user=None, treat_as_anonymous=True):
        return permission_to_view_Q('mediaobject', user, treat_as_anonymous)

    def display_media(self,
                  width=settings.DEFAULT_IMAGE_WIDTH,
                  height=settings.DEFAULT_IMAGE_HEIGHT,
                  html_attributes_in_img_tag="",
                  link=1,
                  with_caption=0,
                  language=settings.ALL_LANGUAGES[settings.DEFAULT_LANGUAGE_INDEX][0],
                  image_to_display=SLIDESHOW):


        def generate_html_for_single_image(image):
            im = get_thumbnail(image, unicode(width)+'x'+unicode(height), crop='center', quality=85)
            html = ''
            if link:
                html += '<a href="' + self.get_absolute_url() +\
                        '" title="' + self.title +  '" >\n'
            html +=  '<img src="' + im.url + '" ' + \
                html_attributes_in_img_tag + ' alt="' + self.title +\
                        '" />\n'
            if link:
                html += '</a>\n'
            return html



        def display_image():

            images = self.images.all()
            output = ''
            number_of_images = images.count()

            # Not a slideshow. Return only one image.
            if number_of_images == 1 or image_to_display >= 0:

                if image_to_display > number_of_images - 1:
                    image_index = number_of_images - 1
                elif number_of_images == 1:
                    image_index = 0
                else:
                    image_index = image_to_display

                image = images[image_index].image

                output += generate_html_for_single_image(image)

            # Get all the images as images (i.e. no slideshow)
            elif image_to_display == ALL_IMAGES:
                output += '<div id="set-of-images">\n'

                for image_iterator in images:
                    output += '<span class="image">\n'
                    output += generate_html_for_single_image(image_iterator.image)
                    output +='</span>\n'

                output += '</div>\n'

            # Slideshow
            else:
                output += '<div id="slider" style="width: ' + unicode(width) +\
                    'px;' + 'height: ' + unicode(height) + 'px;">\n'
                for image_iterator in images:
                    image = image_iterator.image
                    im = get_thumbnail(image, unicode(width)+'x'+unicode(height), crop='center', quality=85)

                    if link:
                        output += '<a href="' + self.get_absolute_url() +\
                            '" title="' + self.title +  '" >\n'

                    output +=  '<img src="' + im.url + '" ' + \
                        html_attributes_in_img_tag + ' alt="' + self.title + '"'

                    if with_caption:
                        output += 'title="'  + image_iterator.get_caption() + '"'

                    output += '/>\n'

                    if link:
                        output += '</a>\n'
                output += '</div>\n'

            return output

        def display_video():
            output = '<video width="' + unicode(width) + '" height="' +\
                unicode(height) + '" controls '

            if self.preload == 'A':
                output += 'autoplay>'
            elif self.preload == 'N':
                output += 'preload="none">'
            elif self.preload == 'P':
                output += 'preload>'
            else:
                output += '>'

            for video in self.video:
                output += '<source src="'
                ouput += video.video_file
                output +='" '
                if video.html_type_attribute:
                    output += 'type="' + video.html_type_attribute + '"'
                output += '/>'

            output += "</video>"

            return output

        def display_embedded():
            '''Replace width and height parameters of the embedded object with
            the width and height passed as arguments.
            '''
            import re

            width_pattern = re.compile(u'width="\d+"')
            height_pattern = re.compile(u'height="\d+"')

            replacement_width = u'width="' + unicode(width) + u'"'
            replacement_height = u'height="' + unicode(height) + u'"'

            output = width_pattern.sub(replacement_width, self.embedded)
            output = height_pattern.sub(replacement_height, output)

            return output

        if self.media_type == 'I':
            final_output = display_image()
        elif self.media_type == 'V':
            final_output = display_video()
        elif self.media_type == 'E':
            final_output = display_embedded()
        else:
            final_output = ''

        if with_caption:
            final_output += '\n<div class="caption">' +\
                self.get_caption(language) +\
                '</div>'

        return final_output

    display_media.allow_tags = True
    display_media.admin_order_field = 'title'

    def thumbprint(self):
        return self.display_media(
                      settings.DEFAULT_THUMB_IMAGE_WIDTH,
                      settings.DEFAULT_THUMB_IMAGE_HEIGHT,
                      image_to_display=0)

    thumbprint.allow_tags = True
    thumbprint.admin_order_field = 'title'

    def passport(self):
        return self.display_media(
                      settings.DEFAULT_PASSPORT_IMAGE_WIDTH,
                      settings.DEFAULT_PASSPORT_IMAGE_HEIGHT)
    passport.allow_tags = True


    def get_caption(self,
                    language=settings.ALL_LANGUAGES[settings.DEFAULT_LANGUAGE_INDEX][0]):
        return get_caption(self, language)

    @models.permalink
    def get_absolute_url(self):
        return ('media_object_detail_view', (), {
            'slug': self.slug
        })

    def describe(self):
        return _("A media item on this site.\n") + self.get_caption()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Media Object (video, image or slideshow)')
        verbose_name_plural = _('Media Objects (video, image or slideshow)')
        ordering = ['date_last_edited']
        permissions = set_extra_permissions('mediaobject')


class Article(ContentObject):
    """Model for representing articles for publication.

    DOCTESTS
    >>> import datetime
    >>> a = Article.objects.create(title="Test", date_published=datetime.datetime.now()+datetime.timedelta(1,0), publication_stage='P')
    >>> b = Article.objects.create(title="Test", date_published=datetime.datetime.now(), publication_stage='P')
    >>> a.is_published()
    False
    >>> b.is_published()
    True
    >>> Article.objects.filter(Article.permission_to_view_Q()).count()
    1
    """
    date_originally_published = models.DateField(null=True, blank=True,
        help_text='This is the date the article was published in any form. '
        'In most cases, you would leave this blank.')
    purpose_of_edit = models.TextField(blank=True)
    image =  models.ImageField(upload_to=settings.UPLOAD_IMAGES_FOLDER_MASK,
                               blank=True, null=True)
    caption = models.CharField(blank=True, max_length=200)
    primary_media_object = models.ForeignKey(MediaObject, blank=True, null=True,
            verbose_name=_('Image, video or slideshow'),
            help_text=_('This media object will be prominently displayed with '
                        'the article.'))
    blurb = models.TextField(blank=True,
                verbose_name=_('Introduction'),
                help_text=_('Write a short introduction to the main article. '
                            'Typically no more than 100 words. '))
    article_text = models.TextField(blank=True,
                help_text=_('The text that comprises the article is placed here. '
                            'You can also insert images, videos etc.'))
    primary_pullout_quote = models.CharField(blank=True,
            max_length=MAX_LENGTH,
            help_text=_('A short piece of text that '
            'will be prominently displayed'))
    text_format = models.CharField(max_length=1,
                                   choices=TEXT_FORMATS,
                                   default=settings.DEFAULT_TEXT_FORMAT)
    page_break_strategy = models.CharField(max_length=2,
                                    choices=PAGE_BREAK_STRATEGIES,
                                    default='C')
    complexity = models.CharField(max_length=1, default='S',
        choices=COMPLEXITY_CHOICES, blank=True)
    language = models.CharField(max_length=7,
                                choices=ALL_LANGUAGES,
                                default=ALL_LANGUAGES[DEFAULT_LANGUAGE_INDEX][0])
    frontpage = models.BooleanField(default=True)
    sticky = models.BooleanField(default=False)
    comments_allowed = models.BooleanField(default=True)
    further_reading = models.ManyToManyField('WebpageLink', through='FurtherReading',
                        blank=True, null=True)
    subscription_required = models.BooleanField(default=False,
        help_text=_('Check this if only subscribed users may view this article.'))


    @models.permalink
    def get_absolute_url(self):
        return ('pubman.views.article_detail', (), {
            'article_slug': self.slug
        })


    @staticmethod
    def permission_to_view_Q(user=None, treat_as_anonymous=True):
        return permission_to_view_Q('article', user, treat_as_anonymous)



    def check_comments_allowed(self):
        if not self.comments_allowed:
            return False
        if settings.CLOSE_AFTER_DAYS > 0 and self.date_published + timedelta(settings.CLOSE_AFTER_DAYS) < datetime.now():
            return False
        return True

    def describe(self):
        return self.blurb

    #def get_name(self):
    #    return self._meta.verbose_name

    def __unicode__(self):
        authors = self.authors_et_al()
        if authors:
            return self.title + ' ' + ugettext('by') + u' ' + self.authors_et_al()
        else:
            return self.title

    __unicode__.admin_order_field = 'title'

    class Meta:
        ordering = ['-date_last_edited']
        permissions = set_extra_permissions('article')
        verbose_name = 'article'
        verbose_name_plural = 'articles'

class ArticleModerator(CommentModerator):
    """Comment moderation class for Article model.
    """
    enable_field = 'comments_allowed'

    if settings.COMMENTS_MODERATED:
        auto_moderate_field = 'date_published'
    else:
        auto_moderate_field = None

    moderate_after = settings.MODERATION_FREE_DAYS

    if settings.CLOSE_AFTER_DAYS:
        auto_close_field = 'date_published'
    else:
        auto_close_field = None

    close_after = settings.CLOSE_AFTER_DAYS

    email_notification = settings.EMAIL_COMMENTS_TO_STAFF

    def allow(self, comment, content_object, request):
        if settings.COMMENTERS_MUST_BE_AUTHENTICATED and\
        not request.user.is_authenticated():
            return False
        else:
            return super(ArticleModerator,self).allow(comment, content_object, request)

moderator.register(Article, ArticleModerator)


class OutOfDate(models.Model):
    '''Reserved for future use.
    Will represent articles that are out-of-date and superceded by other content.
    '''
    article = models.OneToOneField(Article)
    is_out_of_date = models.BooleanField(default=False)
    referral_url = models.URLField(blank=True)
    referral_url_title = models.CharField(max_length=MAX_LENGTH, blank=True)

    class Meta:
        verbose_name = _('out of date article')
        verbose_name_plural = _('out of date articles')


class HistoricalEdit(models.Model):
    '''Reserved for future use.
    Will be used to track changes to articles.
    '''
    article = models.ForeignKey(Article)
    serialization = models.TextField(blank=True)
    date_edited = models.DateTimeField(default=datetime.today())
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _('historical edit')
        verbose_name_plural = _('historical edits')

class Translation(ContentObject):
    '''Model whose instances are a translation of an article.
    '''
    article = models.ForeignKey(Article)
    language = models.CharField(max_length=7,
                                choices=ALL_LANGUAGES,
                                default=django_settings.LANGUAGE_CODE)
    blurb = models.TextField(blank=True)
    article_text = models.TextField(blank=True)
    text_format = models.CharField(max_length=1,
                                   choices=TEXT_FORMATS,
                                   default=settings.DEFAULT_TEXT_FORMAT)
    primary_pullout_quote = models.CharField(blank=True,
                                                        max_length=MAX_LENGTH)

    def is_published(self):
        return is_published(self)

    @staticmethod
    def permission_to_view_Q(user=None, treat_as_anonymous=True):
        return permission_to_view_Q('translation', user, treat_as_anonymous)

    def describe(self):
        return self.blurb

    @models.permalink
    def get_absolute_url(self):
        return ('translated_article', (), {
            'article_slug': self.article.slug,
            'article_lang': self.language
        })


    def __unicode__(self):
        try:
            i = [l[0] for l in ALL_LANGUAGES].index(self.language)
            language = ALL_LANGUAGES[i][1] + " (" + self.language + ")"
        except:
            language = ugettext('Invalid Language')

        return unicode(self.article) + " / " + self.title + u': ' + language

    class Meta:
        ordering = ['-date_last_edited']
        permissions = set_extra_permissions('translation')
        verbose_name = _('translation')
        verbose_name_plural = ('translations')


class Story(ContentObject):
    """Model for representing a collection of articles.
    """
    primary_media_object = models.ForeignKey(MediaObject, blank=True, null=True)
    blurb = models.TextField(blank=True)
    text_format = models.CharField(max_length=1,
                           choices=TEXT_FORMATS,
                           default=settings.DEFAULT_TEXT_FORMAT)
    display_editors = models.CharField(max_length=1,
        choices=EDITOR_DISPLAY_STYLES,
        default='N',
        help_text=_('Indicate if the editors should not be displayed (default), '
        'whether they should be displayed, or whether they should be displayed '
        'as authors.'))
    number_of_articles_per_page = models.IntegerField(default=0,
        help_text=_('Number of articles to display on the story page.\n'
        'Set this to -1 to use the system default.\n'
        'Set this to 0 to display all articles on one page.'))
    contents_as_ordered_list = models.BooleanField(default=True,
                                help_text=_('Shows contents as an ordered '
                                            'list instead of an unordered one. '))
    language = models.CharField(max_length=7,
                                choices=ALL_LANGUAGES,
                                help_text=_('Not implemented yet. Reserved for future use.'),
                                default=django_settings.LANGUAGE_CODE)
    articles = models.ManyToManyField(Article, through='OrderedArticle',
                blank=True, null=True,
                help_text=_('Select articles that make up this story and order '
                            'by putting numbers corresponding to their order '
                            'in the order field.'))

    @models.permalink
    def get_absolute_url(self):
        return ('pubman.views.story_detail', (), {
            'story_slug': self.slug
        })

    @staticmethod
    def permission_to_view_Q(user=None, treat_as_anonymous=True):
        return permission_to_view_Q('story', user, treat_as_anonymous)


    def byline(self):
        if self.display_editors == 'N':
            return ''
        elif self.display_editors == 'E':
            byline_preposition = ugettext('edited by')
        else:
            byline_preposition = ugettext('by')

        authors = self.authors_et_al()

        if authors:
            return byline_preposition + u' ' + authors
        else:
            return ''

    def describe(self):
        return self.blurb

    def article_list(self):
        articles = [orderedarticle.article for orderedarticle in self.orderedarticle_set.all()
            if orderedarticle.article.is_published()]
        return articles

    def __unicode__(self):
        byline = self.byline()
        if byline:
            return self.title + ' ' + byline
        else:
            return self.title

    __unicode__.admin_order_field = 'title'
    __unicode__.allow_tags = True

    class Meta:
        verbose_name_plural = _('stories')
        ordering = ['date_last_edited']
        permissions = set_extra_permissions('story')
        verbose_name = _('story')
        verbose_name_plural = _('stories')

class OrderedArticle(models.Model):
    """Model for representing ordered set of articles within a story.
    """
    story = models.ForeignKey('Story')
    article = models.ForeignKey('Article')
    order = models.IntegerField(default=0,
                                blank = True,
                                null = True,
                                help_text=_('Enter a number indicating '\
                                'first author, second author etc.'))

    def __unicode__(self):
        return self.story.__unicode__() + u': ' + self.article.__unicode__()

    class Meta:
        ordering = ['story','order',]
        unique_together = ('story', 'article', 'order')
        verbose_name = _('ordered article')
        verbose_name_plural = _('ordered articles')


class FeaturedStory(models.Model):
    """Model for indicating which stories should be featured,
    for example on the front page of the website.
    """
    story = models.OneToOneField('Story')
    featured = models.BooleanField(default=True,
        help_text='When this story is no longer featured, set to false '
            'instead of deleting this record')
    order = models.IntegerField(default=0,
                                help_text=_('The lower this number '
                                            'the higher the priority of '
                                            'the story'))
    lead_in_text = models.TextField(help_text=_('Text to introduce story'))
    read_more_message = models.CharField(default=_('Read more ...'),
                                blank=True,
                                max_length=MAX_LENGTH,
                                help_text=_('Message for link to take users '
                                            'to story. Leave blank if you '
                                            'do not want this link.'))
    show_primary_media_object = models.BooleanField(default=False)
    show_contents = models.BooleanField(default=False,
                                help_text=_('Check this if you want the contents of the '
                                            'story displayed.'))
    def is_featured(self):
        return self.story.is_published() and self.featured

    @staticmethod
    def is_featured_Q():
        return Q(featured=True) &\
            Q(story__publication_stage='P') &\
            Q(story__date_published__lte=datetime.now())

    def __unicode__(self):
        return self.story.__unicode__()

    class Meta:
        verbose_name = _('featured story')
        verbose_name_plural = _('featured stories')
        ordering = ['order',]

class FeaturedWebpageGroup(models.Model):
    """This is the parent model that ties together ExternalLinks and LinkOrder
    """
    title = models.CharField(max_length=MAX_LENGTH)
    media_object = models.ForeignKey(MediaObject, blank=True, null=True)
    lead_in_text = models.TextField(blank=True)

    display_primary_media = models.BooleanField(default=False,
                    help_text=_('Check this if you want '
                    'the primary media objects for each link displayed. '
                    'It might not be practical to do this given the way most '
                    'websites are designed.')
                                                                    )
    display_blurbs = models.BooleanField(default=True,
                    verbose_name = _('display link descriptions'),
                    help_text=_('Check this if you want '
                    'the link descriptions displayed.'))

    featured = models.BooleanField(default=True,
                help_text=_('Instead of deleting a group '
                            'when you no longer wish to '
                            'feature this group, rather '
                            'uncheck this field.'))

    order = models.IntegerField(default=0,
                                help_text=_('Determines position of this web '
                                'page group relative to others.'))


    date_last_edited = models.DateTimeField(auto_now=True, editable=False)

    def webpages(self):
        orderedpages = self.orderedwebpage_set.all().order_by('order')
        pages = [i.webpage for i in orderedpages ]
        return pages

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('group of featured web pages')
        verbose_name_plural = _('groups of featured web pages')
        ordering = ['order',]

class WebpageLink(models.Model):
    """Represents manually maintained links to external web pages for display,
    say, on the front page of a website.
    """
    title = models.CharField(max_length=MAX_LENGTH)
    url = models.CharField(max_length=MAX_LENGTH, verbose_name=_('Link'),
                help_text=_('To refer to an article, use the '
                            'article\'s unique id (an integer) '
                            'or its slug. '
                            'To refer to a story, refer to the '
                            'story\'s unique id or slug, but '
                            'prefix with "story:". '
                            'For a page on this site, '
                            'prefix the relative URL with "local:" '
                            'Use a URL of another site to refer to an '
                            'external page.'),
                            validators=[validate_link])
    byline = models.CharField(blank=True, max_length=MAX_LENGTH,
                    help_text=_('The institution or organisation '
                                'that produces this website. There is no '
                                'problem with leaving this blank.'))
    date = models.DateField(blank=True, null=True,
                    help_text=_('Sometimes it is useful to include the '
                                'date a blog was written. But mostly this '
                                'field will be left blank.'))
    html_A_tag_options = models.CharField(max_length=MAX_LENGTH, blank=True,
                                  help_text=_('You can put link, title and other '
                                              'HTML A tag attributes here. '
                                              'Leave blank if you are unsure.'))
    description = models.TextField(blank=True)
    media_object = models.ForeignKey(MediaObject, blank=True, null=True)
    date_last_edited = models.DateTimeField(auto_now=True, editable=False)

    def get_link(self):
        return get_link(self.url)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['date_last_edited',]
        verbose_name = _('webpage')
        verbose_name_plural = _('webpages')


class FurtherReading(models.Model):
    '''Model for representing additional reading links that can be attached
    to articles.
    '''
    article = models.ForeignKey(Article)
    url = models.ForeignKey(WebpageLink,
                            verbose_name=_('link'))
    category = models.CharField(max_length=2,
                                choices=TYPES_OF_FURTHER_READING,
                                default='05')
    order = models.IntegerField(default=0, blank=True, null=True)

    def get_link(self):
        return self.url.get_link()

    def __unicode__(self):
        return unicode(self.article) + u' - '  + unicode(self.url)

    class Meta:
        verbose_name = _("further reading")
        verbose_name_plural = _("further reading")
        ordering = ('category', 'order',)


class OrderedWebpage(models.Model):
    """Model to specify the order of external links for a FeaturedExternalLink
    object.
    """
    featured_webpage_group = models.ForeignKey(FeaturedWebpageGroup)
    webpage = models.ForeignKey(WebpageLink)
    order = models.IntegerField(blank = True,
                                null = True,
                                help_text=_('Determines position of this link '\
                                'in this group.'))

    class Meta:
        verbose_name = _('ordered webpage')
        verbose_name_plural = _('ordered webpages')
        unique_together = ('featured_webpage_group','webpage' )
        ordering = ['order',]

class FeaturedRSSFeed(models.Model):
    """Extremely simple model for user-specified RSS that uses Univerval Feed
    Parser library.

    For anything complex with feeds, this will have to significantly expanded
    upon, probably using Feedjack.
    """
    title = models.CharField(max_length=MAX_LENGTH)
    feed_rss_url = models.URLField(verify_exists=False,
                                  help_text=_('Paste the URL of the '
                                              'RSS feed here.'))
    media_object = models.ForeignKey(MediaObject, blank=True, null=True)
    lead_in_text = models.TextField(blank=True)
    number_of_items = models.IntegerField(default=settings.DEFAULT_RSS_READER_ITEMS)
    display_item_descriptions = models.BooleanField(default=True)
    allow_html_in_item_descriptions = models.BooleanField(default=False)
    item_description_truncate = models.IntegerField(default=0,
            help_text=_('Set this to the maximum number of words in the description '
            'to display. Set to 0 for unlimited.'))
    order = models.IntegerField(default=0,
                                help_text=_('Determines position of this RSS feed '\
                                'relative to others.'))
    featured = models.BooleanField(default=True,
                help_text=_('Instead of deleting a feed '
                            'when you no longer wish to '
                            'use it, rather '
                            'uncheck this field.'))
    date_last_edited = models.DateTimeField(auto_now=True, editable=False)

    def rss_items(self):

        feed = feedparser.parse(self.feed_rss_url)

        if len(feed["items"]) == 0:
            return None
        else:
            return feed["items"][0:self.number_of_items]


    def __unicode__(self):
        return self.title


    class Meta:
        ordering = ['order',]
        verbose_name = _('featured rss feed')
        verbose_name_plural = _('featured rss feeds')

