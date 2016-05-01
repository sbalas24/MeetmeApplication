# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_mmnotification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mmnotification',
            old_name='meeting_id',
            new_name='meeting',
        ),
    ]
