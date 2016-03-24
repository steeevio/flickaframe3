from django.db import models
from time import time
import datetime
import urllib3
import urllib
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

def get_upload_file_name(instance, filename):
	return "uploaded-files/%s-%s" % (str(time()).replace('.','-'), urllib.parse.quote(filename, safe='/', encoding=None, errors=None).lower().replace('_','-'))

def get_upload_avatar_name(instance, filename):
	return "uploaded-avatars/%s-%s" % (str(time()).replace('.','-'), filename)	

def get_upload_group_image_name(instance, filename):
	return "uploaded-group-images/%s-%s" % (str(time()).replace('.','-'), filename)		

def get_upload_draw_image_name(instance, filename):
	return "uploaded-draw-images/%s-%s" % (str(time()).replace('.',''), filename)		

def get_upload_tag_image_name(instance, filename):
	return "uploaded-tag-images/%s-%s" % (str(time()).replace('.','-'), filename)

def get_upload_poster_image_name(instance, filename):
	return "uploaded-poster-images/%s-%s" % (str(time()).replace('.','-'), filename)	

def get_upload_slide_image_name(instance, filename):
	return "uploaded-slide-images/%s-%s" % (str(time()).replace('.','-'), filename)	



class UserProfile(models.Model):
	user_auth = models.OneToOneField(User, primary_key=True)
	phone  = models.CharField(max_length=20, verbose_name = "Phone number", null = True, default = None, blank = True)
	last_connection = models.DateTimeField(null=True, blank=True, default=None, verbose_name = "Date of last connection")
#	member = models.ForeignKey(Group, verbose_name= "member of group", default = None, null = True)
	#user_avatar = models.FileField(upload_to = get_upload_file_name, null= True)
	avatar = models.ImageField(upload_to = get_upload_avatar_name, null= True, default='uploaded-avatars/default.jpg')
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	user_status = models.IntegerField(default = 1, verbose_name = 'Paid status', blank = True, null = True, help_text="1: Free account, 2: Paid Account")
	#1 is free
	#2 is paid level 1
	#3 is paid level 2... later

	#tag_image = models.ImageField(verbose_name = "Tag drawing", upload_to = get_upload_poster_image_name, null = True)
	def __str__(self):
		return self.user_auth.username

class Vid(models.Model):
	def __str__(self):
		return self.video_title
	base_group =  models.OneToOneField('SocialGroup', verbose_name="base_group", null = True, blank = True, default = None)
	video_title = models.CharField(verbose_name = "Title",  max_length = 200, null = True)
	pub_date = models.DateTimeField('date published', null = True, blank=True)
	video_description = models.CharField(verbose_name = "Video Description", max_length = 500, null = True, blank=True)
	video_location = models.CharField(verbose_name = "Location", max_length = 200, null = True, blank=True)
	video_file = models.FileField(upload_to = get_upload_file_name, null= True, blank = True, default = None)
	user = models.ForeignKey(User, verbose_name="User", null = True)
	poster = models.ImageField(verbose_name = "Video poster", upload_to = get_upload_poster_image_name, null = True, default='uploaded-poster-images/default_poster.jpg')
	youtube_id = models.CharField(verbose_name = "Youtube id", max_length = 80, null = True, default = None, blank = True)
	poster_time = models.IntegerField(verbose_name = "Selected poster time", default = 0, blank = True, null = True,)
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	private = models.BooleanField(default = False, help_text = 'True:Only owner can make group, False: anyone can make groups')
	class Meta:
		ordering = ('-updated', 'video_title')

	#def _get_poster(self):
	#	if self.tag_set.tag_image:
	#		try:
	#		poster_get = self.tag_set.all()[0].tag_image
	#		return poster_get
	#	else: 
	#		poster_get = models.ImageField(verbose_name = "Video poster", upload_to = get_upload_poster_image_name, null = True, default='uploaded_poster_images/default_poster.jpg')
	#		return poster_get
	#poster = property(_get_poster)

class Tag(models.Model):
	def __str__(self):
		return self.tag_title
	video = models.ForeignKey(Vid, verbose_name="Video", null = True)
	tag_title = models.CharField(verbose_name = "Tag title", max_length = 200, null = True)
	tag_description = models.CharField(verbose_name = "Tag Description", max_length = 1000, null = True, blank=True)
	tag_start = models.DecimalField(verbose_name = "start time percent", default=0, max_digits=5, decimal_places=2)
	time_secs = models.IntegerField(verbose_name = "Time in seconds", default = 0, blank = True)
	pub_date = models.DateTimeField(verbose_name = "Date Created", auto_now_add = True)
	tag_start_string = models.CharField(verbose_name = "Time of tag", max_length = 50, null = True)
	tag_image = models.ImageField(verbose_name = "Tag image", upload_to = get_upload_tag_image_name, null = True, blank=True)
#	def filename(self):
#		return os.path.basename(self.tag_image.name)
	tag_draw = models.ImageField(verbose_name = "Tag drawing", upload_to = get_upload_draw_image_name, null = True, blank=True)
	user = models.ForeignKey(User, verbose_name = "User", null = True)
	group_tags = models.ForeignKey('SocialGroup', verbose_name ="Tag group", null = True, related_name='tag_groups', default = None, blank = True)
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	tag_moderation = models.IntegerField(help_text = '1: undecided, 2: approved, 3:declined', verbose_name = "tag moderation", default = 1, blank = True, null=True)
	class Meta:
		ordering = ('time_secs', 'tag_title')

	
		#1 - undecided
		#2 - approved
		#3 - declined
		#4 - declined & notified - change to this once it has been viewed on the users profile page


class SocialGroup(models.Model):
	group_owner = models.ForeignKey(User, verbose_name ="Group Owner", null = True, related_name='group_owner', default = None, blank = True)
	group_title = models.CharField(max_length =200, null =True, verbose_name = "Group Title")
	group_description = models.CharField(max_length = 1000, null= True, verbose_name = "Group description")
	group_video = models.ManyToManyField(Vid, verbose_name = "Group Video", related_name='group_video', default = None, blank = True)
	group_member = models.ManyToManyField(User, verbose_name ="group_members", related_name='group_member', through = 'Membership', default = None, blank = True)
	group_images = models.ImageField(upload_to = get_upload_group_image_name, null= True, default = 'uploaded-group-images/default.jpg')
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	group_moderation = models.IntegerField(help_text = '1: no moderation, 2: require moderation', verbose_name = "Group moderation", default = 1, blank = True, null=True)

	group_drawing = models.IntegerField(default = 1, verbose_name = 'allow drawing', blank = True, null = True, help_text="1: deny drawing, 2: allow drawing")
	#1 = stop members drawing - (managers can draw?)
	#2 = allow members to draw
	group_hidden = models.IntegerField(default = 1, verbose_name = 'Hidden status', blank = True, null = True, help_text="1: show group, 2: Members Only")
	#1 = show group to all non members
	#2 = hide group to non members
	#3.. future
	group_access = models.IntegerField(help_text="1:anyone joins, 2:requires approval, 3:invite only", verbose_name = "Who can join", default = 1, blank = True, null=True)
#1 - anyone can join
#2 - I want to approve requests to join
#3 - Only people I invite can join - 
#4 - future ... people who pay can join - earn money for group owner
	group_privacy = models.IntegerField(help_text="1:anyone sees tags, 2: members see tags", verbose_name = "group tags privacy", default = 1, blank = True, null=True)
#1 - Anyone can see the tags
#2 - Only people in the group can see the tags 
#3 - hide the group entirely from non members

	group_taggers = models.IntegerField(help_text="1: members tag, 2:managers tag", verbose_name = "group taggers", default = 1, blank = True, null=True)
#1 - members can tag
#2 - only managers can tag

	def __str__(self):
		return self.group_title

class Membership(models.Model):
	member = models.ForeignKey(User, on_delete = models.CASCADE)
	group = models.ForeignKey(SocialGroup, on_delete = models.CASCADE)
	manager = models.NullBooleanField(default=False, blank = True, null = True)
	membership_status = models.IntegerField(verbose_name = "status", default = 0, blank = True)
	#1 = requested to join
	#2 = accepted
	#3 = rejected to join
	#4 = invited to join
	#5 = invite rejected      
	#6 = group manage
	#7 = sometimes in views use - loggedin but no membership object created

class GroupSlide(models.Model):
	slide_creator = models.ForeignKey(User, verbose_name = "File Created by", null = True, related_name='file_creator', default = None, blank = True)
	slide_name = models.CharField(max_length = 200, null = True, verbose_name = "File Name")
	slide_group = models.ForeignKey(SocialGroup, verbose_name="Slide group", null = True )
	slide_image = models.ImageField(upload_to = get_upload_slide_image_name, null= True, default='uploaded-slide-images/default.jpg')
	slide_tag = models.ForeignKey(Tag, verbose_name="file tag", blank=True, related_name = "tag_slide", default = None, null = True)
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.slide_name

class Comment(models.Model):
	commenter = models.ForeignKey(User, verbose_name = "Comment by", null = True, related_name='commenter', default = None, blank = True)
	message = models.CharField(max_length = 200, null = True, blank=True, default=None, verbose_name = "Message")
	comment_group =  models.ForeignKey(SocialGroup, verbose_name = "group for comment", null = True, related_name='comment_groups', default = None, blank = True)
	comment_video = models.ForeignKey(Vid, verbose_name = "comment video", null = True, related_name='comment_videos', default = None, blank = True)
	comment_tag = models.ForeignKey(Tag, verbose_name = "The tag", null = True, related_name='comment_tags', default = None, blank = True)
	parent_comment = models.ForeignKey('self', null = True, blank = True, on_delete = models.CASCADE, related_name= 'parent_comments', verbose_name = "Parent comment")
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-added', 'message')

	def __str__(self):
		return self.message

class Collection(models.Model):
	collection_creator = models.ForeignKey(User, verbose_name = "Collection Created by", null = True, related_name='collection_creator', default = None, blank = True)
	collection_name = models.CharField(max_length = 200, null = True, verbose_name = "Collection Name")
	collection_description = models.CharField(max_length = 1000, null= True, verbose_name = "collection description")
	collection_tags = models.ManyToManyField(Tag, verbose_name = "Collection Tags", related_name='tag_collection', default = None, blank = True)
	collection_groups = models.ManyToManyField(SocialGroup, verbose_name = "Collection_groups", related_name='group_collection', default = None, blank = True)
	collection_followers = models.ManyToManyField(User, verbose_name = "Collection Followers", related_name='follow_connection', default = None, blank = True)
	collection_admins = models.ManyToManyField(User, verbose_name = "Collection Admins", related_name='admin_collection', default = None, blank = True)

	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-added', 'collection_name')

	def __str__(self):
		return self.collection_name
