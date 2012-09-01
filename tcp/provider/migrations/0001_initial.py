# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Provider'
        db.create_table('provider_provider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('link_template', self.gf('django.db.models.fields.TextField')()),
            ('embed_template', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('provider', ['Provider'])

        # Adding model 'LinkMatch'
        db.create_table('provider_linkmatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['provider.Provider'])),
            ('pattern', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('provider', ['LinkMatch'])


    def backwards(self, orm):
        # Deleting model 'Provider'
        db.delete_table('provider_provider')

        # Deleting model 'LinkMatch'
        db.delete_table('provider_linkmatch')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['provider']