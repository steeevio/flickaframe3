# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import video.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('message', models.CharField(null=True, verbose_name='Message', default=None, max_length=200, blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-added', 'message'),
            },
        ),
        migrations.CreateModel(
            name='GroupSlide',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('slide_name', models.CharField(null=True, max_length=200, verbose_name='File Name')),
                ('slide_image', models.ImageField(null=True, upload_to=video.models.get_upload_slide_image_name, default='uploaded_slide_images/default.jpg')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('manager', models.NullBooleanField(default=False)),
                ('membership_status', models.IntegerField(verbose_name='status', default=0, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialGroup',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('group_title', models.CharField(null=True, max_length=200, verbose_name='Group Title')),
                ('group_description', models.CharField(null=True, max_length=1000, verbose_name='Group description')),
                ('group_images', models.ImageField(null=True, upload_to=video.models.get_upload_group_image_name, default='uploaded_group_images/default.jpg')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('group_moderation', models.IntegerField(null=True, help_text='1: no moderation, 2: require moderation', verbose_name='Group moderation', default=1, blank=True)),
                ('group_drawing', models.IntegerField(null=True, help_text='1: deny drawing, 2: allow drawing', verbose_name='allow drawing', default=1, blank=True)),
                ('group_hidden', models.IntegerField(null=True, help_text='1: show group, 2: Members Only', verbose_name='Hidden status', default=1, blank=True)),
                ('group_access', models.IntegerField(null=True, help_text='1:anyone joins, 2:requires approval, 3:invite only', verbose_name='Who can join', default=1, blank=True)),
                ('group_privacy', models.IntegerField(null=True, help_text='1:anyone sees tags, 2: members see tags', verbose_name='group tags privacy', default=1, blank=True)),
                ('group_taggers', models.IntegerField(null=True, help_text='1: members tag, 2:managers tag', verbose_name='group taggers', default=1, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('tag_title', models.CharField(null=True, max_length=200, verbose_name='Tag title')),
                ('tag_description', models.CharField(null=True, verbose_name='Tag Description', max_length=1000, blank=True)),
                ('tag_start', models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='start time percent')),
                ('time_secs', models.IntegerField(verbose_name='Time in seconds', default=0, blank=True)),
                ('pub_date', models.DateTimeField(verbose_name='Date Created', auto_now_add=True)),
                ('tag_start_string', models.CharField(null=True, max_length=50, verbose_name='Time of tag')),
                ('tag_image', models.ImageField(null=True, upload_to=video.models.get_upload_tag_image_name, verbose_name='Tag image', blank=True)),
                ('tag_draw', models.ImageField(null=True, upload_to=video.models.get_upload_draw_image_name, verbose_name='Tag drawing', blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tag_moderation', models.IntegerField(null=True, help_text='1: undecided, 2: approved, 3:declined', verbose_name='tag moderation', default=1, blank=True)),
                ('group_tags', models.ForeignKey(related_name='tag_groups', default=None, verbose_name='Tag group', null=True, blank=True, to='video.SocialGroup')),
            ],
            options={
                'ordering': ('time_secs', 'tag_title'),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_auth', models.OneToOneField(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(null=True, verbose_name='Phone number', default=None, max_length=20, blank=True)),
                ('last_connection', models.DateTimeField(null=True, verbose_name='Date of last connection', default=None, blank=True)),
                ('avatar', models.ImageField(null=True, upload_to=video.models.get_upload_avatar_name, default='uploaded_group_images/default.jpg')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user_status', models.IntegerField(null=True, help_text='1: Free account, 2: Paid Account', verbose_name='Paid status', default=1, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vid',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('video_title', models.CharField(null=True, max_length=200, verbose_name='Title')),
                ('pub_date', models.DateTimeField(null=True, verbose_name='date published', blank=True)),
                ('video_description', models.CharField(null=True, verbose_name='Video Description', max_length=500, blank=True)),
                ('video_location', models.CharField(null=True, verbose_name='Location', max_length=200, blank=True)),
                ('video_file', models.FileField(null=True, upload_to=video.models.get_upload_file_name, default=None, blank=True)),
                ('poster', models.ImageField(null=True, upload_to=video.models.get_upload_poster_image_name, default='uploaded_poster_images/default_poster.jpg', verbose_name='Video poster')),
                ('youtube_id', models.CharField(null=True, verbose_name='Youtube id', default=None, max_length=80, blank=True)),
                ('poster_time', models.IntegerField(null=True, verbose_name='Selected poster time', default=0, blank=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('private', models.BooleanField(help_text='True:Only owner can make group, False: anyone can make groups', default=False)),
                ('base_group', models.OneToOneField(default=None, blank=True, null=True, verbose_name='base_group', to='video.SocialGroup')),
                ('user', models.ForeignKey(verbose_name='User', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', 'video_title'),
            },
        ),
        migrations.AddField(
            model_name='tag',
            name='user',
            field=models.ForeignKey(verbose_name='User', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tag',
            name='video',
            field=models.ForeignKey(verbose_name='Video', null=True, to='video.Vid'),
        ),
        migrations.AddField(
            model_name='socialgroup',
            name='group_member',
            field=models.ManyToManyField(blank=True, default=None, verbose_name='group_members', related_name='group_member', through='video.Membership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='socialgroup',
            name='group_owner',
            field=models.ForeignKey(related_name='group_owner', default=None, verbose_name='Group Owner', null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='socialgroup',
            name='group_video',
            field=models.ManyToManyField(related_name='group_video', verbose_name='Group Video', default=None, to='video.Vid', blank=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='group',
            field=models.ForeignKey(to='video.SocialGroup'),
        ),
        migrations.AddField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupslide',
            name='slide_creator',
            field=models.ForeignKey(related_name='file_creator', default=None, verbose_name='File Created by', null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupslide',
            name='slide_group',
            field=models.ForeignKey(verbose_name='Slide group', null=True, to='video.SocialGroup'),
        ),
        migrations.AddField(
            model_name='groupslide',
            name='slide_tag',
            field=models.ForeignKey(related_name='tag_slide', default=None, verbose_name='file tag', null=True, blank=True, to='video.Tag'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_group',
            field=models.ForeignKey(related_name='comment_groups', default=None, verbose_name='group for comment', null=True, blank=True, to='video.SocialGroup'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_tag',
            field=models.ForeignKey(related_name='comment_tags', default=None, verbose_name='The tag', null=True, blank=True, to='video.Tag'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_video',
            field=models.ForeignKey(related_name='comment_videos', default=None, verbose_name='comment video', null=True, blank=True, to='video.Vid'),
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(related_name='commenter', default=None, verbose_name='Comment by', null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(related_name='parent_comments', verbose_name='Parent comment', null=True, blank=True, to='video.Comment'),
        ),
    ]
