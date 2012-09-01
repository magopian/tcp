# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = [('provider', '0001_initial')]

    def forwards(self, orm):
        # Adding model 'Request'
        db.create_table('core_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('initial_code', self.gf('django.db.models.fields.TextField')()),
            ('video_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('is_valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('clean_code', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['provider.Provider'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Request'])


    def backwards(self, orm):
        # Deleting model 'Request'
        db.delete_table('core_request')


    models = {
        'core.request': {
            'Meta': {'object_name': 'Request'},
            'clean_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_code': ('django.db.models.fields.TextField', [], {}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['provider.Provider']", 'null': 'True', 'blank': 'True'}),
            'video_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'provider.provider': {
            'Meta': {'object_name': 'Provider'},
            'embed_template': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_template': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['core']
