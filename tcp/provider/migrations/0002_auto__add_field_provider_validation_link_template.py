# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Provider.validation_link_template'
        db.add_column('provider_provider', 'validation_link_template',
                      self.gf('django.db.models.fields.TextField')(default='to compute{{ video_id }}'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Provider.validation_link_template'
        db.delete_column('provider_provider', 'validation_link_template')


    models = {
        'provider.linkmatch': {
            'Meta': {'object_name': 'LinkMatch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['provider.Provider']"})
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

    complete_apps = ['provider']