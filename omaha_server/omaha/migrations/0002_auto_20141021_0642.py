# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import omaha.models


class Migration(migrations.Migration):

    dependencies = [
        ('omaha', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='dsa_signature',
            field=models.CharField(help_text=b'Only for sparkle update', max_length=140, null=True, verbose_name=b'DSA signature', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='version',
            name='file',
            field=models.FileField(upload_to=omaha.models.version_upload_to),
        ),
    ]
