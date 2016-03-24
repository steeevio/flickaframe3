# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import video.models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20160307_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupslide',
            name='slide_image',
            field=models.ImageField(default='uploaded-slide-images/default.jpg', upload_to=video.models.get_upload_slide_image_name, null=True),
        ),
        migrations.AlterField(
            model_name='socialgroup',
            name='group_images',
            field=models.ImageField(default='uploaded-group-images/default.jpg', upload_to=video.models.get_upload_group_image_name, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='uploaded-avatars/default.jpg', upload_to=video.models.get_upload_avatar_name, null=True),
        ),
        migrations.AlterField(
            model_name='vid',
            name='poster',
            field=models.ImageField(default='uploaded-poster-images/default_poster.jpg', upload_to=video.models.get_upload_poster_image_name, null=True, verbose_name='Video poster'),
        ),
    ]
