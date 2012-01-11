# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Article.image'
        db.add_column('pubman_article', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'Article.caption'
        db.add_column('pubman_article', 'caption', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Article.image'
        db.delete_column('pubman_article', 'image')

        # Deleting field 'Article.caption'
        db.delete_column('pubman_article', 'caption')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pubman.article': {
            'Meta': {'ordering': "['-date_last_edited']", 'object_name': 'Article'},
            'article_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comments_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'complexity': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.Copyright']", 'null': 'True', 'blank': 'True'}),
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_originally_published': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 10, 19, 11, 4, 87418)', 'null': 'True', 'blank': 'True'}),
            'frontpage': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'further_reading': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pubman.WebpageLink']", 'null': 'True', 'through': "orm['pubman.FurtherReading']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '7'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page_break_strategy': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '2'}),
            'primary_media_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.MediaObject']", 'null': 'True', 'blank': 'True'}),
            'primary_pullout_quote': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'publication_stage': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'purpose_of_edit': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subscription_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'text_format': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'users_who_can_edit_this': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'pubman.caption': {
            'Meta': {'ordering': "['-date_last_edited']", 'object_name': 'Caption'},
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '7'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'pubman.copyright': {
            'Meta': {'ordering': "['title']", 'object_name': 'Copyright'},
            'easy_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'html_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legal_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'pubman.credit': {
            'Meta': {'object_name': 'Credit'},
            'first_names': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_person': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tags': ('tagging.fields.TagField', [], {})
        },
        'pubman.featuredrssfeed': {
            'Meta': {'ordering': "['order']", 'object_name': 'FeaturedRSSFeed'},
            'allow_html_in_item_descriptions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'display_item_descriptions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'feed_rss_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_description_truncate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lead_in_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'media_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.MediaObject']", 'null': 'True', 'blank': 'True'}),
            'number_of_items': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'pubman.featuredstory': {
            'Meta': {'ordering': "['order']", 'object_name': 'FeaturedStory'},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead_in_text': ('django.db.models.fields.TextField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'read_more_message': ('django.db.models.fields.CharField', [], {'default': "u'Read more ...'", 'max_length': '200', 'blank': 'True'}),
            'show_contents': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_primary_media_object': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'story': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['pubman.Story']", 'unique': 'True'})
        },
        'pubman.featuredwebpagegroup': {
            'Meta': {'ordering': "['order']", 'object_name': 'FeaturedWebpageGroup'},
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'display_blurbs': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'display_primary_media': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead_in_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'media_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.MediaObject']", 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'pubman.furtherreading': {
            'Meta': {'ordering': "('category', 'order')", 'object_name': 'FurtherReading'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.Article']"}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'05'", 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.WebpageLink']"})
        },
        'pubman.historicaledit': {
            'Meta': {'object_name': 'HistoricalEdit'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.Article']"}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 10, 19, 11, 4, 96561)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'serialization': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'pubman.image': {
            'Meta': {'ordering': "['-date_last_edited']", 'object_name': 'Image'},
            'captions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pubman.Caption']", 'null': 'True', 'blank': 'True'}),
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'pubman.mediaobject': {
            'Meta': {'ordering': "['date_last_edited']", 'object_name': 'MediaObject'},
            'captions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pubman.Caption']", 'null': 'True', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.Copyright']", 'null': 'True', 'blank': 'True'}),
            'date_captured': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 10, 19, 11, 4, 87418)', 'null': 'True', 'blank': 'True'}),
            'embedded': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pubman.Image']", 'null': 'True', 'blank': 'True'}),
            'media_type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '2'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'preload': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '2'}),
            'publication_stage': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'users_who_can_edit_this': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'video_files': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pubman.Video']", 'null': 'True', 'blank': 'True'})
        },
        'pubman.orderedarticle': {
            'Meta': {'ordering': "['story', 'order']", 'unique_together': "(('story', 'article', 'order'),)", 'object_name': 'OrderedArticle'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.Story']"})
        },
        'pubman.orderedcredit': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('content_type', 'object_id', 'author_or_institution'),)", 'object_name': 'OrderedCredit'},
            'author_or_institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.Credit']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'pubman.orderedwebpage': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('featured_webpage_group', 'webpage'),)", 'object_name': 'OrderedWebpage'},
            'featured_webpage_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.FeaturedWebpageGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'webpage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.WebpageLink']"})
        },
        'pubman.outofdate': {
            'Meta': {'object_name': 'OutOfDate'},
            'article': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['pubman.Article']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_out_of_date': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'referral_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'referral_url_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'pubman.story': {
            'Meta': {'ordering': "['date_last_edited']", 'object_name': 'Story'},
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pubman.Article']", 'null': 'True', 'through': "orm['pubman.OrderedArticle']", 'blank': 'True'}),
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contents_as_ordered_list': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'copyright': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.Copyright']", 'null': 'True', 'blank': 'True'}),
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 10, 19, 11, 4, 87418)', 'null': 'True', 'blank': 'True'}),
            'display_editors': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '7'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number_of_articles_per_page': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'primary_media_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.MediaObject']", 'null': 'True', 'blank': 'True'}),
            'publication_stage': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'text_format': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'users_who_can_edit_this': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'pubman.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'date_from': ('django.db.models.fields.DateField', [], {}),
            'date_to': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.UserProfile']"})
        },
        'pubman.translation': {
            'Meta': {'ordering': "['-date_last_edited']", 'object_name': 'Translation'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.Article']"}),
            'article_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'copyright': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.Copyright']", 'null': 'True', 'blank': 'True'}),
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 10, 19, 11, 4, 87418)', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '7'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'primary_pullout_quote': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'publication_stage': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'text_format': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'users_who_can_edit_this': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'pubman.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'avatar': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'physical_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'physical_address_city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'physical_address_code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'physical_address_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'blank': 'True'}),
            'postal_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'postal_address_city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'postal_address_code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'postal_address_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'pubman.video': {
            'Meta': {'object_name': 'Video'},
            'html_type_attribute': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'video_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'pubman.webpagelink': {
            'Meta': {'ordering': "['date_last_edited']", 'object_name': 'WebpageLink'},
            'byline': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'html_A_tag_options': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.MediaObject']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pubman']
