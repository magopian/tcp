# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Request.is_valid'
        db.delete_column('core_request', 'is_valid')

        # Deleting field 'Request.video_link'
        db.delete_column('core_request', 'video_link')

        # Deleting field 'Request.message'
        db.delete_column('core_request', 'message')

        # Deleting field 'Request.clean_code'
        db.delete_column('core_request', 'clean_code')


    def backwards(self, orm):
        # Adding field 'Request.is_valid'
        db.add_column('core_request', 'is_valid',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Request.video_link'
        db.add_column('core_request', 'video_link',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Request.message'
        db.add_column('core_request', 'message',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Request.clean_code'
        db.add_column('core_request', 'clean_code',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    models = {
        'core.request': {
            'Meta': {'object_name': 'Request'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_code': ('django.db.models.fields.TextField', [], {}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['provider.Provider']", 'null': 'True', 'blank': 'True'}),
            'video_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'provider.provider': {
            'Meta': {'object_name': 'Provider'},
            'embed_template': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_template': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'validation_link_template': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['core']