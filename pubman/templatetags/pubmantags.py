from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.template.defaultfilters import urlize, linebreaks
from django.contrib.markup.templatetags.markup import markdown, restructuredtext

from pubman import settings
from pubman.models import MediaObject, SLIDESHOW 

register = template.Library()

@register.simple_tag
def format_content(value, format):

    
    if format=='M': # markdown
        value = markdown(value, settings.MARKDOWN_EXTENSIONS)
    elif format == 'R':
        value = restructuredtext(value) 
    elif format=='H':
        value = mark_safe(value)
    else:
        value = linebreaks(urlize(escape(value)))
            
    return value
    
format_content.needs_autoescape = True


@register.simple_tag
def display_media(mediaobject, 
                  width=settings.DEFAULT_IMAGE_WIDTH, 
                  height=settings.DEFAULT_IMAGE_HEIGHT,
                  html_attributes_in_img_tag="",
                  link=1,
                  with_caption=0,
                  language=settings.ALL_LANGUAGES[settings.DEFAULT_LANGUAGE_INDEX][0],
                  image_to_display=SLIDESHOW):

    if mediaobject == None:
        return ""
    
    if not isinstance(mediaobject, MediaObject):
        try:
            int(mediaobject)
        except ValueError:
            return "" # Fail silently if the object is wrong type
        else:
            try:
                mediaobject = MediaObject.objects.get(id=mediaobject)
            except ObjectDoesNotExist:
                return "" # Fail silently if the object is wrong type

    # Using *args instead of named arguments throws a Template Exception. Not sure why.
    return mediaobject.display_media(width, 
                                     height, 
                                     html_attributes_in_img_tag, 
                                     link,
                                     with_caption,
                                     language,
                                     image_to_display)
    
display_media.needs_autoescape = True
