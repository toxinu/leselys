# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Folder'
        db.create_table(u'reader_folder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'reader', ['Folder'])

        # Adding model 'Story'
        db.create_table(u'reader_story', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('published', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('readed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reader.Feed'])),
        ))
        db.send_create_signal(u'reader', ['Story'])

        # Adding model 'Feed'
        db.create_table(u'reader_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('custom_title', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('website_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('favicon_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('ordering', self.gf('django.db.models.fields.SmallIntegerField')(default=0, blank=True)),
            ('folder', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['reader.Folder'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('in_error', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('error', self.gf('django.db.models.fields.CharField')(default=u'This feed has never been fetched', max_length=1000, blank=True)),
        ))
        db.send_create_signal(u'reader', ['Feed'])


    def backwards(self, orm):
        # Deleting model 'Folder'
        db.delete_table(u'reader_folder')

        # Deleting model 'Story'
        db.delete_table(u'reader_story')

        # Deleting model 'Feed'
        db.delete_table(u'reader_feed')


    models = {
        u'reader.feed': {
            'Meta': {'object_name': 'Feed'},
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'custom_title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'error': ('django.db.models.fields.CharField', [], {'default': "u'This feed has never been fetched'", 'max_length': '1000', 'blank': 'True'}),
            'favicon_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['reader.Folder']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_error': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ordering': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'reader.folder': {
            'Meta': {'object_name': 'Folder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reader.story': {
            'Meta': {'object_name': 'Story'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reader.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'readed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['reader']
