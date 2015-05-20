# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ParliamentMember'
        db.create_table('mps_v2_parliamentmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('source_id', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('date_of_birth', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('candidate_page', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('raised_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps_v2.PoliticalParty'])),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('term_of_office', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('office_address', self.gf('django.db.models.fields.TextField')()),
            ('constituency', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('party_candidate', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('mps_v2', ['ParliamentMember'])

        # Adding model 'PoliticalParty'
        db.create_table('mps_v2_politicalparty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('mps_v2', ['PoliticalParty'])

        # Adding model 'Group'
        db.create_table('mps_v2_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('mps_v2', ['Group'])

        # Adding model 'GroupMembership'
        db.create_table('mps_v2_groupmembership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps_v2.ParliamentMember'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mps_v2.Group'])),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('since', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('mps_v2', ['GroupMembership'])


    def backwards(self, orm):
        # Deleting model 'ParliamentMember'
        db.delete_table('mps_v2_parliamentmember')

        # Deleting model 'PoliticalParty'
        db.delete_table('mps_v2_politicalparty')

        # Deleting model 'Group'
        db.delete_table('mps_v2_group')

        # Deleting model 'GroupMembership'
        db.delete_table('mps_v2_groupmembership')


    models = {
        'mps_v2.group': {
            'Meta': {'object_name': 'Group'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'source': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['mps_v2']