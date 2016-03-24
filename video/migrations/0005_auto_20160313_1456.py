# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import video.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0004_auto_20160310_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('collection_name', models.CharField(verbose_name='Collection Name', null=True, max_length=200)),
                ('collection_description', models.CharField(verbose_name='collection description', null=True, max_length=1000)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('collection_admins', models.ManyToManyField(verbose_name='Collection Admins', to=settings.AUTH_USER_MODEL, blank=True, related_name='admin_collection', default=None)),
                ('collection_followers', models.ManyToManyField(verbose_name='Collection Followers', to=settings.AUTH_USER_MODEL, blank=True, related_name='follow_connection', default=None)),
            ],
            options={
                'ordering': ('-added', 'collection_name'),
            },
        ),
        migrations.AlterField(
            model_name='socialgroup',
            name='group_images',
            field=models.ImageField(upload_to=video.models.get_upload_group_image_name, null=True, default='uploaded-group-images/default.jpg'),
        ),
        migrations.AddField(
            model_name='collection',
            name='collection_groups',
            field=models.ManyToManyField(verbose_name='Collection_groups', to='video.SocialGroup', blank=True, related_name='group_collection', default=None),
        ),
        migrations.AddField(
            model_name='collection',
            name='collection_tags',
            field=models.ManyToManyField(verbose_name='Collection Tags', to='video.Tag', blank=True, related_name='tag_collection', default=None),
        ),
        migrations.AddField(
            model_name='collection',
            name='model_creator',
            field=models.ForeignKey(verbose_name='Collection Created by', null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='collection_creator', default=None),
        ),
    ]
