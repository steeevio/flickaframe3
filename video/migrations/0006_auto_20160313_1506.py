# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0005_auto_20160313_1456'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='model_creator',
            new_name='collection_creator',
        ),
    ]
