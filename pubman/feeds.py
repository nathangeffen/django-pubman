'''Processes rss and atom feeds for pubman Articles.
'''

import datetime
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

import settings

from models import Article
from siteconfig.context_processors import website 

class LatestArticlesRSSFeed(Feed):
    title = website()['website'].feed_title
    link = "/sitenews/"
    description = website()['website'].feed_description
     
    def items(self):
        return Article.objects.filter(publication_stage='P').\
            filter(date_published__lte=datetime.datetime.now()).\
            filter(frontpage=True).\
            order_by('-date_published')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.blurb

class LatestArticlesAtomFeed(LatestArticlesRSSFeed):
    feed_type = Atom1Feed

    def item_description(self, item):
        return item.subtitle
    
    