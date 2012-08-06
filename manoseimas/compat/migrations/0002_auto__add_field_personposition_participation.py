# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PersonPosition.participation'
        db.add_column('compat_personposition', 'participation',
                      self.gf('django.db.models.fields.DecimalField')(default='1', max_digits=7, decimal_places=4, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PersonPosition.participation'
        db.delete_column('compat_personposition', 'participation')


    models = {
        'compat.personposition': {
            'Meta': {'object_name': 'PersonPosition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('sboard.models.NodeForeignKey', [], {}),
            'participation': ('django.db.models.fields.DecimalField', [], {'default': "'1'", 'max_digits': '7', 'decimal_places': '4', 'db_index': 'True'}),
            'position': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '4', 'db_index': 'True'}),
            'profile': ('sboard.models.NodeForeignKey', [], {}),
            'profile_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['compat']