# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Group', fields ['name']
        db.create_unique('mps_v2_group', ['name'])

        # Adding unique constraint on 'Group', fields ['type', 'name']
        db.create_unique('mps_v2_group', ['type', 'name'])

        # Adding unique constraint on 'PoliticalParty', fields ['name']
        db.create_unique('mps_v2_politicalparty', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'PoliticalParty', fields ['name']
        db.delete_unique('mps_v2_politicalparty', ['name'])

        # Removing unique constraint on 'Group', fields ['type', 'name']
        db.delete_unique('mps_v2_group', ['type', 'name'])

        # Removing unique constraint on 'Group', fields ['name']
        db.delete_unique('mps_v2_group', ['name'])


    models = {
        'mps_v2.group': {
            'Meta': {'unique_together': "(('name', 'type'),)", 'object_name': 'Group'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'mps_v2.groupmembership': {
            'Meta': {'object_name': 'GroupMembership'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps_v2.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps_v2.ParliamentMember']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'since': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'mps_v2.parliamentmember': {
            'Meta': {'object_name': 'ParliamentMember'},
            'candidate_page': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'constituency': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mps_v2.Group']", 'through': "orm['mps_v2.GroupMembership']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'office_address': ('django.db.models.fields.TextField', [], {}),
            'party_candidate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'raised_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mps_v2.PoliticalParty']"}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'term_of_office': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'mps_v2.politicalparty': {
            'Meta': {'object_name': 'PoliticalParty'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['mps_v2']