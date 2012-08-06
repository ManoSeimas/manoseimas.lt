# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PersonPosition'
        db.create_table('compat_personposition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('sboard.models.NodeForeignKey')()),
            ('profile', self.gf('sboard.models.NodeForeignKey')()),
            ('profile_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('position', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=4, db_index=True)),
        ))
        db.send_create_signal('compat', ['PersonPosition'])


    def backwards(self, orm):
        # Deleting model 'PersonPosition'
        db.delete_table('compat_personposition')


    models = {
        'compat.personposition': {
            'Meta': {'object_name': 'PersonPosition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('sboard.models.NodeForeignKey', [], {}),
            'position': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '4', 'db_index': 'True'}),
            'profile': ('sboard.models.NodeForeignKey', [], {}),
            'profile_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['compat']