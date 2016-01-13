# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-13 09:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('new', 'new'), ('proc', 'proc'), ('sent', 'sent'), ('sched', 'sched'), ('err', 'err'), ('read', 'read'), ('unread', 'unread')], db_index=True, default='new', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='MessageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'new'), ('proc', 'proc'), ('sent', 'sent'), ('sched', 'sched'), ('err', 'err'), ('read', 'read'), ('unread', 'unread')], max_length=32)),
                ('request_data', models.TextField()),
                ('response_data', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('timestamp_update', models.DateTimeField(auto_now=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='sms_handler.Message')),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=256)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='messagelog',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='sms_handler.Provider'),
        ),
    ]