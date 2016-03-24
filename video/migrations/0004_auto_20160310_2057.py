# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import video.models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_auto_20160307_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialgroup',
            name='group_images',
            field=models.ImageField(upload_to=video.models.get_upload_group_image_name, default='/uploaded-group-images/default.jpg', null=True),
        ),
    ]
