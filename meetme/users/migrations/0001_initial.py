# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MMcontact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MMcontact_name',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, verbose_name=b'name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MMmeeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('duration', models.CharField(max_length=30, null=True, verbose_name=b'Duration')),
                ('meeting_confirmed', models.BooleanField(default=False)),
                ('meeting_name', models.CharField(max_length=30, verbose_name=b'Meeting Name')),
                ('description', models.CharField(max_length=3000, verbose_name=b'Description', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MMmeetingparticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('required', models.BooleanField(default=True)),
                ('meeting', models.ForeignKey(to='users.MMmeeting')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MMUser',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=30, verbose_name=b'name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='mmmeetingparticipant',
            name='participant',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mmmeeting',
            name='user',
            field=models.ForeignKey(related_name='meeting_host', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='mmcontact',
            name='contact',
            field=models.ForeignKey(related_name='contact', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mmcontact',
            name='user',
            field=models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
