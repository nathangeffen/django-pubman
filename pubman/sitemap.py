'''Creates sitemap for Story, Translation and Article models.
'''

from django.contrib.sitemaps import Sitemap
from models import Article, Story, Translation

class ArticleSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Article.objects.filter(Article.permission_to_view_Q())

    def lastmod(self, obj):
        return obj.date_last_edited

class StorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Story.objects.filter(Story.permission_to_view_Q())

    def lastmod(self, obj):
        return obj.date_last_edited

class TranslationSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Translation.objects.filter(Translation.permission_to_view_Q())

    def lastmod(self, obj):
        return obj.date_last_edited
