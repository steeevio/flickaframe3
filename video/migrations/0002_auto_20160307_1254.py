# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import video.models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='uploaded-group-images/default.jpg', upload_to=video.models.get_upload_avatar_name, null=True),
        ),
    ]
