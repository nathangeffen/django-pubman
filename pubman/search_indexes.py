'''This module implements Haystack indices for searching.  

Search indices have been implemented for Article, MediaObject, Story and 
Copyright.
'''

import datetime
from haystack.indexes import *
from haystack import site
from pubman.models import Article, MediaObject, Story, Copyright, Translation

class ArticleIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='date_published')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Article.objects.filter(Article.permission_to_view_Q())


site.register(Article, ArticleIndex)

class StoryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='date_published')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Story.objects.filter(Story.permission_to_view_Q())

site.register(Story, StoryIndex)

class MediaObjectIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='date_published')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return MediaObject.objects.filter(MediaObject.permission_to_view_Q())


site.register(MediaObject, MediaObjectIndex)

class TranslationIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='date_published')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Translation.objects.filter(Translation.permission_to_view_Q())


site.register(Translation, TranslationIndex)


class CopyrightIndex(SearchIndex):
    text = CharField(document=True, use_template=True)

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Copyright.objects.all()


site.register(Copyright, CopyrightIndex)
    