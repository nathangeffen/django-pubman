# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('pubman_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('avatar', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('physical_address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('physical_address_code', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('physical_address_city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('physical_address_country', self.gf('django_countries.fields.CountryField')(max_length=2, blank=True)),
            ('postal_address', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('postal_address_code', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('postal_address_city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('postal_address_country', self.gf('django_countries.fields.CountryField')(max_length=2, blank=True)),
        ))
        db.send_create_signal('pubman', ['UserProfile'])

        # Adding model 'Subscription'
        db.create_table('pubman_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.UserProfile'])),
            ('date_from', self.gf('django.db.models.fields.DateField')()),
            ('date_to', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('pubman', ['Subscription'])

        # Adding model 'Copyright'
        db.create_table('pubman_copyright', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('easy_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('legal_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('html_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('pubman', ['Copyright'])

        # Adding model 'Credit'
        db.create_table('pubman_credit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_person', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('first_names', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal('pubman', ['Credit'])

        # Adding model 'OrderedCredit'
        db.create_table('pubman_orderedcredit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author_or_institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.Credit'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('pubman', ['OrderedCredit'])

        # Adding unique constraint on 'OrderedCredit', fields ['content_type', 'object_id', 'author_or_institution']
        db.create_unique('pubman_orderedcredit', ['content_type_id', 'object_id', 'author_or_institution_id'])

        # Adding model 'Video'
        db.create_table('pubman_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('video_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('html_type_attribute', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('pubman', ['Video'])

        # Adding model 'Caption'
        db.create_table('pubman_caption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=7)),
            ('date_last_edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('pubman', ['Caption'])

        # Adding model 'Image'
        db.create_table('pubman_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('date_last_edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('pubman', ['Image'])

        # Adding M2M table for field captions on 'Image'
        db.create_table('pubman_image_captions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('image', models.ForeignKey(orm['pubman.image'], null=False)),
            ('caption', models.ForeignKey(orm['pubman.caption'], null=False))
        ))
        db.create_unique('pubman_image_captions', ['image_id', 'caption_id'])

        # Adding model 'MediaObject'
        db.create_table('pubman_mediaobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('date_published', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 1, 10, 19, 10, 9, 781627), null=True, blank=True)),
            ('publication_stage', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200, db_index=True)),
            ('copyright', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.Copyright'], null=True, blank=True)),
            ('date_last_edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('media_type', self.gf('django.db.models.fields.CharField')(default='I', max_length=2)),
            ('preload', self.gf('django.db.models.fields.CharField')(default='D', max_length=2)),
            ('embedded', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_captured', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('pubman', ['MediaObject'])

        # Adding M2M table for field users_who_can_edit_this on 'MediaObject'
        db.create_table('pubman_mediaobject_users_who_can_edit_this', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mediaobject', models.ForeignKey(orm['pubman.mediaobject'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('pubman_mediaobject_users_who_can_edit_this', ['mediaobject_id', 'user_id'])

        # Adding M2M table for field images on 'MediaObject'
        db.create_table('pubman_mediaobject_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mediaobject', models.ForeignKey(orm['pubman.mediaobject'], null=False)),
            ('image', models.ForeignKey(orm['pubman.image'], null=False))
        ))
        db.create_unique('pubman_mediaobject_images', ['mediaobject_id', 'image_id'])

        # Adding M2M table for field video_files on 'MediaObject'
        db.create_table('pubman_mediaobject_video_files', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mediaobject', models.ForeignKey(orm['pubman.mediaobject'], null=False)),
            ('video', models.ForeignKey(orm['pubman.video'], null=False))
        ))
        db.create_unique('pubman_mediaobject_video_files', ['mediaobject_id', 'video_id'])

        # Adding M2M table for field captions on 'MediaObject'
        db.create_table('pubman_mediaobject_captions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mediaobject', models.ForeignKey(orm['pubman.mediaobject'], null=False)),
            ('caption', models.ForeignKey(orm['pubman.caption'], null=False))
        ))
        db.create_unique('pubman_mediaobject_captions', ['mediaobject_id', 'caption_id'])

        # Adding model 'Article'
        db.create_table('pubman_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('date_published', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 1, 10, 19, 10, 9, 781627), null=True, blank=True)),
            ('publication_stage', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200, db_index=True)),
            ('copyright', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.Copyright'], null=True, blank=True)),
            ('date_last_edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('date_originally_published', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('purpose_of_edit', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('primary_media_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.MediaObject'], null=True, blank=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('article_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('primary_pullout_quote', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('text_format', self.gf('django.db.models.fields.CharField')(default='H', max_length=1)),
            ('page_break_strategy', self.gf('django.db.models.fields.CharField')(default='C', max_length=2)),
            ('complexity', self.gf('django.db.models.fields.CharField')(default='S', max_length=1, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=7)),
            ('frontpage', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comments_allowed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subscription_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('pubman', ['Article'])

        # Adding M2M table for field users_who_can_edit_this on 'Article'
        db.create_table('pubman_article_users_who_can_edit_this', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['pubman.article'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('pubman_article_users_who_can_edit_this', ['article_id', 'user_id'])

        # Adding model 'OutOfDate'
        db.create_table('pubman_outofdate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pubman.Article'], unique=True)),
            ('is_out_of_date', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('referral_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('referral_url_title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('pubman', ['OutOfDate'])

        # Adding model 'HistoricalEdit'
        db.create_table('pubman_historicaledit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.Article'])),
            ('serialization', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 1, 10, 19, 10, 9, 790910))),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('pubman', ['HistoricalEdit'])

        # Adding model 'Translation'
        db.create_table('pubman_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('date_published', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 1, 10, 19, 10, 9, 781627), null=True, blank=True)),
            ('publication_stage', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200, db_index=True)),
            ('copyright', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.Copyright'], null=True, blank=True)),
            ('date_last_edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.Article'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='en-us', max_length=7)),
            ('blurb', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('article_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text_format', self.gf('django.db.models.fields.CharField')(default='H', max_length=1)),
            ('primary_pullout_quote', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('pubman', ['Translation'])

        # Adding M2M table for field users_who_can_edit_this on 'Translation'
        db.create_table('pubman_translation_users_who_can_edit_this', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('translation', models.ForeignKey(orm['pubman.translation'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('pubman_translation_users_who_can_edit_this', ['translation_id', 'user_id'])

        # Adding model 'Story'
        db.create_table('pubman_story', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('date_published', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 1, 10, 19, 10, 9, 781627), null=True, blank=True)),
            ('publication_stage', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200, db_index=True)),
            ('copyright', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.Copyright'], null=True, blank=True)),
            ('date_last_edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('primary_media_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.MediaObject'], null=True, blank=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text_format', self.gf('django.db.models.fields.CharField')(default='H', max_length=1)),
            ('display_editors', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('number_of_articles_per_page', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('contents_as_ordered_list', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en-us', max_length=7)),
        ))
        db.send_create_signal('pubman', ['Story'])

        # Adding M2M table for field users_who_can_edit_this on 'Story'
        db.create_table('pubman_story_users_who_can_edit_this', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('story', models.ForeignKey(orm['pubman.story'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('pubman_story_users_who_can_edit_this', ['story_id', 'user_id'])

        # Adding model 'OrderedArticle'
        db.create_table('pubman_orderedarticle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.Story'])),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.Article'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('pubman', ['OrderedArticle'])

        # Adding unique constraint on 'OrderedArticle', fields ['story', 'article', 'order']
        db.create_unique('pubman_orderedarticle', ['story_id', 'article_id', 'order'])

        # Adding model 'FeaturedStory'
        db.create_table('pubman_featuredstory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('story', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pubman.Story'], unique=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lead_in_text', self.gf('django.db.models.fields.TextField')()),
            ('read_more_message', self.gf('django.db.models.fields.CharField')(default=u'Read more ...', max_length=200, blank=True)),
            ('show_primary_media_object', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_contents', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('pubman', ['FeaturedStory'])

        # Adding model 'FeaturedWebpageGroup'
        db.create_table('pubman_featuredwebpagegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('media_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.MediaObject'], null=True, blank=True)),
            ('lead_in_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('display_primary_media', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('display_blurbs', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_last_edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('pubman', ['FeaturedWebpageGroup'])

        # Adding model 'WebpageLink'
        db.create_table('pubman_webpagelink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('byline', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('html_A_tag_options', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('media_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.MediaObject'], null=True, blank=True)),
            ('date_last_edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('pubman', ['WebpageLink'])

        # Adding model 'FurtherReading'
        db.create_table('pubman_furtherreading', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.Article'])),
            ('url', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.WebpageLink'])),
            ('category', self.gf('django.db.models.fields.CharField')(default='05', max_length=2)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('pubman', ['FurtherReading'])

        # Adding model 'OrderedWebpage'
        db.create_table('pubman_orderedwebpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('featured_webpage_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.FeaturedWebpageGroup'])),
            ('webpage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.WebpageLink'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('pubman', ['OrderedWebpage'])

        # Adding unique constraint on 'OrderedWebpage', fields ['featured_webpage_group', 'webpage']
        db.create_unique('pubman_orderedwebpage', ['featured_webpage_group_id', 'webpage_id'])

        # Adding model 'FeaturedRSSFeed'
        db.create_table('pubman_featuredrssfeed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('feed_rss_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('media_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pubman.MediaObject'], null=True, blank=True)),
            ('lead_in_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('number_of_items', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('display_item_descriptions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('allow_html_in_item_descriptions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('item_description_truncate', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_last_edited', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('pubman', ['FeaturedRSSFeed'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'OrderedWebpage', fields ['featured_webpage_group', 'webpage']
        db.delete_unique('pubman_orderedwebpage', ['featured_webpage_group_id', 'webpage_id'])

        # Removing unique constraint on 'OrderedArticle', fields ['story', 'article', 'order']
        db.delete_unique('pubman_orderedarticle', ['story_id', 'article_id', 'order'])

        # Removing unique constraint on 'OrderedCredit', fields ['content_type', 'object_id', 'author_or_institution']
        db.delete_unique('pubman_orderedcredit', ['content_type_id', 'object_id', 'author_or_institution_id'])

        # Deleting model 'UserProfile'
        db.delete_table('pubman_userprofile')

        # Deleting model 'Subscription'
        db.delete_table('pubman_subscription')

        # Deleting model 'Copyright'
        db.delete_table('pubman_copyright')

        # Deleting model 'Credit'
        db.delete_table('pubman_credit')

        # Deleting model 'OrderedCredit'
        db.delete_table('pubman_orderedcredit')

        # Deleting model 'Video'
        db.delete_table('pubman_video')

        # Deleting model 'Caption'
        db.delete_table('pubman_caption')

        # Deleting model 'Image'
        db.delete_table('pubman_image')

        # Removing M2M table for field captions on 'Image'
        db.delete_table('pubman_image_captions')

        # Deleting model 'MediaObject'
        db.delete_table('pubman_mediaobject')

        # Removing M2M table for field users_who_can_edit_this on 'MediaObject'
        db.delete_table('pubman_mediaobject_users_who_can_edit_this')

        # Removing M2M table for field images on 'MediaObject'
        db.delete_table('pubman_mediaobject_images')

        # Removing M2M table for field video_files on 'MediaObject'
        db.delete_table('pubman_mediaobject_video_files')

        # Removing M2M table for field captions on 'MediaObject'
        db.delete_table('pubman_mediaobject_captions')

        # Deleting model 'Article'
        db.delete_table('pubman_article')

        # Removing M2M table for field users_who_can_edit_this on 'Article'
        db.delete_table('pubman_article_users_who_can_edit_this')

        # Deleting model 'OutOfDate'
        db.delete_table('pubman_outofdate')

        # Deleting model 'HistoricalEdit'
        db.delete_table('pubman_historicaledit')

        # Deleting model 'Translation'
        db.delete_table('pubman_translation')

        # Removing M2M table for field users_who_can_edit_this on 'Translation'
        db.delete_table('pubman_translation_users_who_can_edit_this')

        # Deleting model 'Story'
        db.delete_table('pubman_story')

        # Removing M2M table for field users_who_can_edit_this on 'Story'
        db.delete_table('pubman_story_users_who_can_edit_this')

        # Deleting model 'OrderedArticle'
        db.delete_table('pubman_orderedarticle')

        # Deleting model 'FeaturedStory'
        db.delete_table('pubman_featuredstory')

        # Deleting model 'FeaturedWebpageGroup'
        db.delete_table('pubman_featuredwebpagegroup')

        # Deleting model 'WebpageLink'
        db.delete_table('pubman_webpagelink')

        # Deleting model 'FurtherReading'
        db.delete_table('pubman_furtherreading')

        # Deleting model 'OrderedWebpage'
        db.delete_table('pubman_orderedwebpage')

        # Deleting model 'FeaturedRSSFeed'
        db.delete_table('pubman_featuredrssfeed')


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
            'comments_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'complexity': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pubman.Copyright']", 'null': 'True', 'blank': 'True'}),
            'date_last_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_originally_published': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 10, 19, 10, 9, 781627)', 'null': 'True', 'blank': 'True'}),
            'frontpage': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'further_reading': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pubman.WebpageLink']", 'null': 'True', 'through': "orm['pubman.FurtherReading']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 10, 19, 10, 9, 790910)'}),
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
            'date_published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 10, 19, 10, 9, 781627)', 'null': 'True', 'blank': 'True'}),
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
            'date_published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 10, 19, 10, 9, 781627)', 'null': 'True', 'blank': 'True'}),
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
            'date_published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 10, 19, 10, 9, 781627)', 'null': 'True', 'blank': 'True'}),
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
