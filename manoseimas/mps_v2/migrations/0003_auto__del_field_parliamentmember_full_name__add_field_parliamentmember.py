# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ParliamentMember.full_name'
        db.delete_column('mps_v2_parliamentmember', 'full_name')

        # Adding field 'ParliamentMember.first_name'
        db.add_column('mps_v2_parliamentmember', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)

        # Adding field 'ParliamentMember.last_name'
        db.add_column('mps_v2_parliamentmember', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)

        # Adding field 'ParliamentMember.biography'
        db.add_column('mps_v2_parliamentmember', 'biography',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ParliamentMember.full_name'
        raise RuntimeError("Cannot reverse this migration. 'ParliamentMember.full_name' and its values cannot be restored.")
        # Deleting field 'ParliamentMember.first_name'
        db.delete_column('mps_v2_parliamentmember', 'first_name')

        # Deleting field 'ParliamentMember.last_name'
        db.delete_column('mps_v2_parliamentmember', 'last_name')

        # Deleting field 'ParliamentMember.biography'
        db.delete_column('mps_v2_parliamentmember', 'biography')


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
            'biography': ('django.db.models.fields.TextField', [], {}),
            'candidate_page': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'constituency': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mps_v2.Group']", 'through': "orm['mps_v2.GroupMembership']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
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