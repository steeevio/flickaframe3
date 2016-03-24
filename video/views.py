from django.shortcuts import get_object_or_404, render, render_to_response
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from requests import request, ConnectionError

from urllib.parse import urlparse
import urllib.request
from django.core.files import File
from django.core.files.storage import default_storage as storage




from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import CheckboxSelectMultiple
from easy_thumbnails.files import get_thumbnailer
from django.core.files.base import ContentFile
from itertools import chain

from django.db.models import Q




from.models import Vid, Tag, UserProfile, Collection, Comment, SocialGroup, GroupSlide, Membership, get_upload_draw_image_name, get_upload_avatar_name
from django import forms
from video.forms import UploadForm
from video.forms import GroupForm
from video.forms import EditTagForm
from video.forms import SlideForm
from video.forms import CollectionForm
from video.forms import GroupOptionsForm
from django import forms
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login #import neccesary function for login authentication
from django.contrib.auth import logout

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required


from django.core.serializers.json import DjangoJSONEncoder
import json
#import re
import base64


def comment(request, social_group_id = 0, tag_id = 0, vid_id = 0, tag_time = 0):
	tag_id_int = int(tag_id)
	vid_id_int = int(vid_id)
	social_group_id_int = int(social_group_id)

	user = request.user

	#levels : 1 = tag comment , 2= video comment, 3 = group coment, 4 = reply to a comment
	if request.method == "POST":
		group_id = request.POST.get('group')
		comment = request.POST.get('comment')
		parent_id = request.POST.get('parent')
		level = request.POST.get('level')
		
		response_data = {}
		response_data['comment'] = comment
		response_data['parent_id'] = parent_id

		response_data['level'] = level
		response_data['user_name'] = user.username
		response_data['user_avatar'] = user.userprofile.avatar.name

		if social_group_id_int > 0:
			group = get_object_or_404(SocialGroup, pk = social_group_id)

		if tag_id_int > 0:	
			tag = get_object_or_404(Tag, pk = tag_id)
			video = tag.video

		if vid_id_int > 0:
			video = get_object_or_404(Vid, pk = vid_id)	
			group_id_int = int(group_id)
			group = get_object_or_404(SocialGroup, pk = group_id_int)	

		level_int = int(level)



		if level_int == 1:	#its a  tag level so save to all - tag, vid and group
			save_comment = Comment(commenter = user, message = comment, comment_group = group, comment_video = video, comment_tag = tag)
			save_comment.save()	

		if level_int == 2: #its a  video level so save to vid and group
			save_comment = Comment(commenter = user, message = comment, comment_group = group, comment_video = video)
			save_comment.save()	

		if level_int == 3: #its a  group level so save to group
			save_comment = Comment(commenter = user, message = comment, comment_group = group)
			save_comment.save()	

		if level_int == 4: #its a reply so just saves to parent
			parent_comment = get_object_or_404(Comment, pk = parent_id)
			save_comment = Comment(commenter = user, message = comment, parent_comment = parent_comment)
			save_comment.save()	

		comment_id = save_comment.id
		#this_comment = get_object_or_404(Comment, pk = comment_id)
		response_data['comment_id'] = comment_id
		return HttpResponse(
				json.dumps(response_data),
				content_type = "application/json"
				)

	else:
		return HttpResponse("Somethings wrong here!!pP")


def index(request):
	user = request.user
	video_list = Vid.objects.order_by('-pub_date')[:10]
	user_list = User.objects.order_by('id')[:10]
	group_list = SocialGroup.objects.order_by('id')[:10]
	context = {'video_list': video_list, 'user_list':user_list, 'group_list':group_list, 'user':user}
	return render(request, 'video/index.html', context)


def log_out(request):
	logout(request)
	auth_logout(request)
	return render(request, 'video/logout.html')



def connection(request):
	if request.POST:
		form  = Form_connection(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user = authenticate(username=username, password=password) # username and password are correct

			if user: # returns none if validation failed otherwise returns an object so validates the condition
				login(request, user) # login() function allows the user to connect
		else:
			return render (request, 'video/connection.html',  {'form':form})
		return HttpResponseRedirect("/video/user_profile/%s/" % user.id)		
	else:
		form = Form_connection()
		return render (request, 'video/connection.html',  {'form':form})

class Form_connection(forms.Form):
	username = forms.CharField(max_length=30, label = 'login')
	password = forms.CharField(label='password', widget = forms.PasswordInput)
	def clean(self):
		cleaned_data = super(Form_connection, self).clean()
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if not authenticate(username=username, password=password):
			raise forms.ValidationError("incorrect username or password")
		return self.cleaned_data	


#View for creating a group
def create_group(request, vid_id = 0):
	user = request.user
	if request.POST:
		
		form = GroupForm(request.POST, request.FILES)
		if form.is_valid():
			group_title = form.cleaned_data['group_title']
			group_description = form.cleaned_data['group_description']
			group_image = form.cleaned_data['group_images']
			group_video = form.cleaned_data['add_video']
			group_owner = user
			new_group = SocialGroup(group_description = group_description, group_owner = group_owner, group_title = group_title, group_images = group_image)

			new_group.save()
			if group_video != None:
				video = get_object_or_404(Vid, pk = group_video)
				new_group.group_video.add(video)

			m1 = Membership.objects.create(group = new_group, member = group_owner, membership_status = 6, manager = True)
			return HttpResponseRedirect("/video/social_group/%s/" % new_group.id)
		else:
			return HttpResponse("Aomethings wrong here")


	else:
		form = GroupForm(request.POST)
		args = {'user':user}
		#pass the video id to the template if we have come from a video
		if int(vid_id) > 0:
			group_video = vid_id
			args = {'user':user}
			video = get_object_or_404(Vid, pk = group_video)
			args['video'] = video
		
		args = {'user':user}
		args.update(csrf(request))
		args['form'] = form
		return render_to_response('video/create_group.html/', args)


class Form_user(forms.Form):
	name = forms.CharField(label="Name", max_length = 40)
	login = forms.CharField(label="Login")
	email = forms.EmailField(label="Email")
	avatar = forms.ImageField(label="Avatar")
	password = forms.CharField(label="password", widget = forms.PasswordInput)
	password_bis = forms.CharField(label="password", widget = forms.PasswordInput)
	def clean(self):
		cleaned_data = super (Form_user, self).clean()
		password = self.cleaned_data.get('password')
		password_bis = self.cleaned_data.get('password_bis')
		if password and password_bis and password != password_bis:
			raise forms.ValidationError("Passwords don't match")
		return self.cleaned_data	

#simple home view testing redirect after twitter login
@login_required(login_url='/')
def home(request):
	return render_to_response('home.html')

#view for saving a profile from a social login
def save_profile_social(backend, user, response, is_new,  *args, **kwargs):
	'''
	Get the user avatar (and any other details you're interested in)
	and save them to the userprofile
	'''
	if backend.name == 'facebook':   # and is_new:
		try:
			prof = user.userprofile
		except:		
			prof = UserProfile(user_auth = user)
			prof.save()
			
			#url = 'http://graph.facebook.com/%s/picture' % (id)

			try:
				url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

				response = request('GET', url, params={'type': 'large'})
				response.raise_for_status()
			except ConnectionError:
				pass
			else:
				prof.avatar.save(u'', ContentFile(response.content), save=False)
				prof.save()
				#response.raise_for_status()
'''	elif backend.name == 'google-plus':
			try:
				prof = user.userprofile
			except:		
				prof = UserProfile(user_auth = user)
				prof.save()
			
				if response.get('image') and response['image'].get('url'):
					url = response['image'].get('url')
		 
		            if prof.avatar:
		                # if existing avatar stick with it rather than google syncing
		                pass
		            else:
		                try:
		                    response = request('GET', url)
		                    response.raise_for_status()
		                except ConnectionError:
		                    pass
		                else:
		                    # No avatar so sync it with the google one.
		                    # Passing '' for name will invoke my upload_to function
		                    # saving by username (you prob want to change this!)
		                    prof.avatar.save(u'',
		                                    ContentFile(response.content),
		                                    save=False
		                                    )
		                    prof.save()			'''
			

#creating an account the old fashioned way
def create_user_account(request):
	if request.POST:
		form = Form_user(request.POST, request.FILES)
		if form.is_valid():
			name = form.cleaned_data['name']
			avatar = form.cleaned_data['avatar']
			login = form.cleaned_data['login']
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			new_user = User.objects.create_user(username = login, email = email, password = password, )
			new_user.is_active = True # active defines whether user can connect or not - default is false - thn you could make active by email etc
			new_user.last_name = name # define the name of the new user
			new_user.save()
			new_user_profile = UserProfile(user_auth = new_user, avatar = avatar)
			new_user_profile.save()

			#sending email notification "You have been invited..." - first attempt
			#send_mail(subject, message, from_email, to_list, fail_silently = True)
			subject = 'TagFrame: User created'
			message = 'You have created a user'
			from_email = settings.EMAIL_HOST_USER
			to_list = [email, settings.EMAIL_HOST_USER]
			send_mail(subject, message, from_email, to_list, fail_silently=False)

			return HttpResponseRedirect('/video/connection') # need to pass a message here that has
			# account has been created - now please login - maybe need to validate email first
		else:
			return render(request, 'video/create_user.html', {'form':form} )	
	else: 
	#form = Form_user()	
		form = Form_user()	
	return render(request, 'video/create_user.html',  {'form':form} )




class FormUserSelectGroup(forms.ModelForm):

		

	group_member = forms.ModelMultipleChoiceField(
		SocialGroup.objects.all(),
		widget = FilteredSelectMultiple(
			'group_members',
			False,
		))

	class Meta:
		model = User
		fields = ('group_member',)

	class Media:
		css = {'all': ('/static/video/admin/css/widgets.css',),}
		js = ( '/admin/jsi18n',)



	def __init__(self, *args, **kwargs):
		super(FormUserSelectGroup, self).__init__(*args, **kwargs)
		if self.instance.pk:
			self.initial['group_member'] = self.instance.group_member.values_list('pk', flat=True)

	def save(self, *args, **kwargs):
		instance = super(FormUserSelectGroup, self).save(*args, **kwargs)
		if instance.pk:
			instance.group_member.clear()
			instance.group_member.add(*self.cleaned_data['group_member'])
			return instance

		#for member in self.cleaned_data.get('group_member'):
		#	member.group_member.add(self.instance)
		#return super(FormUserSelectGroup, self).save(*args, **kwargs)	




def user_profile(request, user_profile_id):
	number = str(user_profile_id)
	user_profile =  get_object_or_404(User, pk = user_profile_id)
	videos  = Vid.objects.filter(user = user_profile)[:6]
	groups = SocialGroup.objects.filter(Q(group_member = user_profile) | Q(group_owner = user_profile))[:6] 
	collections = Collection.objects.filter(collection_creator = user_profile)[:6]
	slides = GroupSlide.objects.filter(slide_creator = user_profile)[:6]
	tags = Tag.objects.filter(user = user_profile)[:6]
	current_user = request.user

	test_current_user = current_user.id
	test_profile_user = user_profile.id
	
	# a list of all of the memberships associated with this user which have a status = 4 i.e invited to join
	group_invites = SocialGroup.objects.filter(membership__member = user_profile, membership__membership_status = 4)
	if request.user.is_authenticated():
		#if the logged in user matches the userprofile page this_user=True
		if test_current_user == test_profile_user:
			this_user = True
		else:
			this_user = False

	else:
		this_user = False	

	context = {'slides':slides, 'collections':collections, 'test_current_user':test_current_user, 'test_profile_user':test_profile_user, 'videos': videos, 'user_profile':user_profile, 'groups':groups, 'tags':tags, 'number':number, 'this_user':this_user, 'group_invites':group_invites,}

	return render(request, 'video/user_profile.html', context)	


def user_profile_slides(request, user_profile_id):
	number = str(user_profile_id)
	user_profile =  get_object_or_404(User, pk = user_profile_id)
	videos  = Vid.objects.filter(user = user_profile)
	groups = SocialGroup.objects.filter(group_member = user_profile)
	tags = Tag.objects.filter(user = user_profile)
	current_user = request.user
	slides = GroupSlide.objects.filter(slide_creator = user_profile)
	test_current_user = current_user.id
	test_profile_user = user_profile.id
	
	# a list of all of the memberships associated with this user which have a status = 4 i.e invited to join
	group_invites = SocialGroup.objects.filter(membership__member = user_profile, membership__membership_status = 4)
	if request.user.is_authenticated():
		#if the logged in user matches the userprofile page this_user=True
		if test_current_user == test_profile_user:
			this_user = True
		else:
			this_user = False

	else:
		this_user = False	

	context = { 'slides':slides , 'test_current_user':test_current_user, 'test_profile_user':test_profile_user, 'videos': videos, 'user_profile':user_profile, 'groups':groups, 'tags':tags, 'number':number, 'this_user':this_user, 'group_invites':group_invites,}






	if request.POST:
		form = SlideForm(request.POST, request.FILES)
		if form.is_valid():
			slide_name = form.cleaned_data['slide_name']
			slide_image = form.cleaned_data['slide_image']
			user = request.user
			new_slide = GroupSlide(slide_creator = user, slide_name=slide_name, slide_image = slide_image)
			new_slide.save()

	
			return HttpResponseRedirect('/video/user_profile/%s/slides' % (user.id))

		else:
			return HttpResponse("Aomethings wrong here")	
	else:
		form = SlideForm(request.POST)
		#args = {}
		context.update(csrf(request))
		context['form'] = form

		return render(request, 'video/user_profile_slides.html', context)	
		


def user_profile_collections(request, user_profile_id, tag_id = 0):
	number = str(user_profile_id)
	user_profile =  get_object_or_404(User, pk = user_profile_id)
	groups = SocialGroup.objects.filter(group_member = user_profile)
	tags = Tag.objects.filter(user = user_profile)
	current_user = request.user
	test_current_user = current_user.id
	test_profile_user = user_profile.id
	collections = Collection.objects.filter(collection_creator = user_profile)
	
	# a list of all of the memberships associated with this user which have a status = 4 i.e invited to join
	group_invites = SocialGroup.objects.filter(membership__member = user_profile, membership__membership_status = 4)
	if request.user.is_authenticated():
		#if the logged in user matches the userprofile page this_user=True
		if test_current_user == test_profile_user:
			this_user = True
		else:
			this_user = False

	else:
		this_user = False	
	context = { 'collections':collections , 'test_current_user':test_current_user, 'test_profile_user':test_profile_user, 'user_profile':user_profile, 'groups':groups, 'tags':tags, 'number':number, 'this_user':this_user, 'group_invites':group_invites,}
	
	if request.POST:
		form = CollectionForm(request.POST, request.FILES)
		if form.is_valid():
			collection_name = form.cleaned_data['collection_name']
			collection_description = form.cleaned_data['collection_description']
			collection_tag_id = form.cleaned_data['collection_tag']
			
			user = request.user
			new_collection = Collection(collection_creator = user, collection_name = collection_name, collection_description = collection_description)
			new_collection.save()
			if collection_tag_id != None:
				collection_tag = get_object_or_404(Tag, pk = collection_tag_id)
				new_collection.collection_tags.add(collection_tag)

	
			return HttpResponseRedirect('/video/user_profile/%s/collections' % (user.id))

		else:
			return HttpResponse("Aomethings wrong here")	
	else:

		#pass the tag id to the template if we have come from a tag
		if int(tag_id) > 0:
			#collect_tag = tag_id
			
			tag = get_object_or_404(Tag, pk = tag_id)
			context['tag'] = tag
		

		form = CollectionForm(request.POST)
		#args = {}
		context.update(csrf(request))
		context['form'] = form		



	return render(request, 'video/user_profile_collections.html', context)	



def user_profile_collection_solo(request, user_profile_id, collection_id):
	number = str(user_profile_id)
	user_profile =  get_object_or_404(User, pk = user_profile_id)
	videos  = Vid.objects.filter(user = user_profile)
	groups = SocialGroup.objects.filter(group_member = user_profile)
	collection = get_object_or_404(Collection, pk = collection_id)
	tags = Tag.objects.filter(tag_collection = collection)
	current_user = request.user
	test_current_user = current_user.id
	test_profile_user = user_profile.id
	
	
	# a list of all of the memberships associated with this user which have a status = 4 i.e invited to join
	group_invites = SocialGroup.objects.filter(membership__member = user_profile, membership__membership_status = 4)
	if request.user.is_authenticated():
		#if the logged in user matches the userprofile page this_user=True
		if test_current_user == test_profile_user:
			this_user = True
		else:
			this_user = False

	else:
		this_user = False

	context = { 'tags':tags, 'collection':collection, 'test_current_user':test_current_user, 'test_profile_user':test_profile_user, 'videos': videos, 'user_profile':user_profile, 'groups':groups, 'tags':tags, 'number':number, 'this_user':this_user, 'group_invites':group_invites,}
	

	return render(request, 'video/user_profile_collection_solo.html', context)	




def user_profile_groups(request, user_profile_id):
	number = str(user_profile_id)
	user_profile =  get_object_or_404(User, pk = user_profile_id)
	groups = SocialGroup.objects.filter(group_member = user_profile)
	current_user = request.user
	test_current_user = current_user.id
	test_profile_user = user_profile.id
	# a list of all of the memberships associated with this user which have a status = 4 i.e invited to join
	group_invites = SocialGroup.objects.filter(membership__member = user_profile, membership__membership_status = 4)
	if request.user.is_authenticated():
		#if the logged in user matches the userprofile page this_user=True
		if test_current_user == test_profile_user:
			this_user = True
		else:
			this_user = False
	else:
		this_user = False

	context = { 'test_current_user':test_current_user, 'test_profile_user':test_profile_user, 'user_profile':user_profile, 'groups':groups, 'number':number, 'this_user':this_user, 'group_invites':group_invites,}

	return render(request, 'video/user_profile_groups.html', context)	

def user_profile_tags(request, user_profile_id):
	number = str(user_profile_id)
	user_profile =  get_object_or_404(User, pk = user_profile_id)
	groups = SocialGroup.objects.filter(group_member = user_profile)
	tags = Tag.objects.filter(user = user_profile)
	current_user = request.user
	test_current_user = current_user.id
	test_profile_user = user_profile.id
	# a list of all of the memberships associated with this user which have a status = 4 i.e invited to join
	group_invites = SocialGroup.objects.filter(membership__member = user_profile, membership__membership_status = 4)
	if request.user.is_authenticated():
		#if the logged in user matches the userprofile page this_user=True
		if test_current_user == test_profile_user:
			this_user = True
		else:
			this_user = False
	else:
		this_user = False

	context = { 'tags':tags,'test_current_user':test_current_user, 'test_profile_user':test_profile_user, 'user_profile':user_profile, 'number':number, 'this_user':this_user, 'group_invites':group_invites,}

	return render(request, 'video/user_profile_tags.html', context)	


def user_profile_videos(request, user_profile_id):
	number = str(user_profile_id)
	user_profile =  get_object_or_404(User, pk = user_profile_id)
	groups = SocialGroup.objects.filter(group_member = user_profile)
	current_user = request.user
	test_current_user = current_user.id
	test_profile_user = user_profile.id
	videos  = Vid.objects.filter(user = user_profile)
	# a list of all of the memberships associated with this user which have a status = 4 i.e invited to join
	group_invites = SocialGroup.objects.filter(membership__member = user_profile, membership__membership_status = 4)
	if request.user.is_authenticated():
		#if the logged in user matches the userprofile page this_user=True
		if test_current_user == test_profile_user:
			this_user = True
		else:
			this_user = False
	else:
		this_user = False

	context = {'videos':videos, 'test_current_user':test_current_user, 'test_profile_user':test_profile_user, 'user_profile':user_profile, 'groups':groups, 'number':number, 'this_user':this_user, 'group_invites':group_invites,}

	return render(request, 'video/user_profile_videos.html', context)	


def user_profile_save_groups(request):
	
	number = request.POST['number']
	user_profile =  get_object_or_404(User, pk = number)

	if request.POST:	
		form = FormUserSelectGroup(request.POST, instance = user_profile)
		if form.is_valid():
			form.save()

			return HttpResponse("Groups added")
		else:
			return HttpResponse("Aomethings wrong here")




#view for a video  - integrating different versions
def video(request, vid_id, tag_time = 0, social_group_id = 0, poster_time_str = 0):
	number = str(vid_id)	
	video = get_object_or_404(Vid, pk = vid_id)

	tags = Tag.objects.filter(video = video).exclude(group_tags__group_privacy = 2) 
	group = video.base_group # if no group is set in the url we go to the base group
	groups = SocialGroup.objects.filter(group_video = video)
	tags = tags.prefetch_related('tag_slide').all()
	comments = Comment.objects.filter(comment_video = video).prefetch_related('parent_comment').all()

	if request.user.is_authenticated():
		user = request.user
		groups_accepted = SocialGroup.objects.filter(group_video = video, group_member = user, membership__membership_status = 2)
		groups_manager = SocialGroup.objects.filter(group_video = video, group_member = user, membership__membership_status = 6)
		#just using groups member now to work out which user isnt a member of - passing accepted and manager seperately
		groups_member =  list(chain(groups_accepted, groups_manager))
		not_groups_member = SocialGroup.objects.filter(group_video = video).exclude(group_member = user)
		slides_group = GroupSlide.objects.filter(slide_group__in = groups_member)

		slides_user = GroupSlide.objects.filter(slide_creator = user)
		# exclude tags that user is not a member of and that has a group_privacy status of 2 - members can see the tags
		not_groups_member_private = SocialGroup.objects.filter(group_video = video, group_privacy = 2).exclude(group_member = user)
		# exclude tags that user is not a member of and that has a group_privacy status of 1 - anyone can see the tags
		not_groups_member_open = SocialGroup.objects.filter(group_video = video, group_privacy = 1).exclude(group_member = user)

		#tags exclude unmoderated tags - except those by the current user
		tags = Tag.objects.filter(video = video).exclude(group_tags__in = not_groups_member_private).exclude(~Q(user= user), tag_moderation = 1)
		
#find all of the tags associated with this video that are not in a group non member private


		if Membership.objects.filter(member = user, group = group).exists():
			member_of_group = True

		else:
			member_of_group = False
	else:
		tags = Tag.objects.filter(video = video).exclude(group_tags__group_privacy = 2).exclude(tag_moderation = 1).exclude(tag_moderation = 3) # exclude any private tags when not logged in
		user = None
		groups_member = None
		groups_accepted = None
		groups_manager = None
		not_groups_member = SocialGroup.objects.filter(group_video = video)
		member_of_group = False
		slides_group = None
		slides_user = None
		not_groups_member_private = None
		not_groups_member_open = None

	context = {'not_groups_member_private':not_groups_member_private,'not_groups_member_open':not_groups_member_open, 'groups_manager':groups_manager, 'groups_accepted':groups_accepted, 'group':group, 'comments':comments, 'slides_group':slides_group, 'slides_user':slides_user, 'user':user, 'number': number, 'video':video, 'tags':tags, 'groups':groups, 'groups_member':groups_member, 'not_groups_member':not_groups_member}
	
	if int(tag_time) > 0:
		tag_time = str(tag_time)
		context['tag_time'] = tag_time

	if int(social_group_id) > 0:
		group = get_object_or_404(SocialGroup, pk = social_group_id)
		context['group'] = group

	if int(poster_time_str) > 0:
		script = "window.onload = setPoster(" + poster_time_str + "); "	#we pass a script that starts the video at a certain time
		context['script'] = script	

	#group_taggers = group.group_taggers
	#context['group_taggers'] = group_taggers

	return render(request, 'video/video.html', context)





#Create view for upload video using model

def upload_page(request):
	user = request.user
	if request.POST:
		form = UploadForm(request.POST, request.FILES)
		
		if form.is_valid():
			video_title = form.cleaned_data['video_title']
			video_description = form.cleaned_data['video_description']
			video_file = form.cleaned_data['video_file']
			youtube_id = form.cleaned_data['youtube_id']
			private = form.cleaned_data['private']

			poster_time = form.cleaned_data['poster_time']
			if poster_time:
				if poster_time > 0:
					poster_time_str = str(poster_time)
			else:
				poster_time_str = "5"	
			
			if len(youtube_id) > 5:
				youtube_id = youtube_id.split("?v=")[1]
				new_video = Vid(private = private, youtube_id = youtube_id, video_title = video_title, video_description = video_description, user = user)
			
			if video_file:
				new_video = Vid(private = private, video_title = video_title, video_description = video_description, user = user, video_file = video_file)

			#create the video object			
			new_video.save()

			# create a group linked to this new video
			base_group = SocialGroup(group_owner = user, group_title = "Base Group:" + video_title, group_description = "This is the base group for this video")
			base_group.save()
			base_group.group_video.add(new_video)

			m1 = Membership.objects.create(group = base_group, member = user, membership_status = 6)
			

			#link the base group as a foreign key so we know its the main group for this video - might be a better way to just use the first group for a video
			new_video.base_group = base_group
			new_video.save()
			if len(youtube_id) > 5:
				return HttpResponseRedirect('/video/%s/%s/from_group' % (new_video.id, base_group.id))
			else:
				return HttpResponseRedirect('/video/%s/%s/%s/init' % (new_video.id, base_group.id, poster_time_str))
				
				
					
			
		else:
			return HttpResponse("Aomethings wrong here")	
	else:
		form = UploadForm(request.POST)
		args = {'user':user}
		args.update(csrf(request))
		args['form'] = form
		return render_to_response('video/upload.html/', args)


class Form_tag_delete(forms.Form):
	#we are creating a form so that we can use django validators to check what is being sent - nothing malicous
	tag = forms.IntegerField()
@csrf_exempt # probably need to pull this delete stuff into another view so this csrf isn't an issue

def delete_tag(request, vid_id):
	return_value = 0
	
	form = Form_tag_delete(request.POST)
	if form.is_valid():
		id_tag = form.cleaned_data ['tag']
		tag_record = Tag.objects.get(id=id_tag)
		tag_record.delete()
		return_value = id_tag

	return HttpResponse(json.dumps(return_value),content_type = "application/json")
	



class FormVideoSelect(ModelForm):
	class Meta:
		model = SocialGroup
		fields = ('group_video',)
 

        
''' commented because we no longer use this form - we use ajax
class FormVideoSelectFilter(forms.ModelForm):

	group_video = forms.ModelMultipleChoiceField(
		Vid.objects.all(),
		widget = FilteredSelectMultiple(
			'Group Video',
			False,
			attrs={'rows':'5'},
		))

	class Meta:
		model = SocialGroup
		fields = ('group_video',)

	class Media:
		css = {'all': ('/static/video/admin/css/widgets.css',),}
		js = ('/admin/jsi18n',)

	def save(self, *args, **kwargs):
		instance = super(FormUserSelectGroup, self).save(*args, **kwargs)
		if instance.pk:
			instance.group_video.clear()
			instance.group_video.add(*self.cleaned_data['group_video'])
			return instance
'''


def social_group_settings(request, social_group_id):
	number = str(social_group_id)
	group = get_object_or_404(SocialGroup, pk = social_group_id)
	videos  = Vid.objects.filter(group_video = group)[:6]
	members = User.objects.filter(group_member = group, membership__membership_status = 2)[:6]
	admins = User.objects.filter(group_member = group, membership__membership_status = 6)[:6]
	requested = User.objects.filter(group_member = group, membership__membership_status = 1)
	comments = Comment.objects.filter(comment_group = group).prefetch_related('parent_comment').all()
	unmoderated_tags = Tag.objects.filter(group_tags = group, tag_moderation = 1)


	collections = Collection.objects.filter(collection_groups = group)[:6]
	slides = GroupSlide.objects.filter(slide_group = group)[:6]
	tags = Tag.objects.filter(group_tags = group)[:6]
	# check current users relationship to this group 
	# not currently working because I need to only check the membership status is one already exist...
	if request.user.is_authenticated():
		try:
			user_membership = Membership.objects.get(group = group, member = request.user)
			user_status = user_membership.membership_status
		except:
			user_status = 5	#5 offers the chance to login despite already having a membership

	else:
		user_status = 8 # not logged in

	context = {'admins':admins, 'collections':collections, 'slides':slides, 'tags':tags, 'unmoderated_tags':unmoderated_tags, 'comments':comments, 'number':number, 'videos':videos, 'group':group, 'members':members, 'requested':requested, 'user_status':user_status}
	
	if request.POST:
		form = GroupOptionsForm(request.POST)
		if form.is_valid():
			group_access = form.cleaned_data['group_access']
			group_privacy = form.cleaned_data['group_privacy']
			group_taggers = form.cleaned_data['group_taggers']
			group_title = form.cleaned_data['group_title']
			group_description = form.cleaned_data['group_description']
			group_hidden = form.cleaned_data['group_hidden']
			group_drawing = form.cleaned_data['group_drawing']
			group_moderation = form.cleaned_data['group_moderation']
			group.group_access = int(group_access)
			group.group_privacy = int(group_privacy)
			group.group_taggers = int(group_taggers)
			group.group_moderation = int(group_moderation)
			group.group_title = group_title
			group.group_hidden = group_hidden
			group.group_drawing = int(group_drawing)
			group.group_description = group_description
			group.save()
			init_group_moderation = group.group_moderation
			init_group_access = group.group_access
			init_group_privacy = group.group_privacy
			init_group_taggers = group.group_taggers
			init_group_title = group.group_title
			init_group_description = group.group_description
			init_group_hidden = group.group_hidden
			init_group_drawing = group.group_drawing
			form = GroupOptionsForm(initial={'group_moderation':init_group_moderation, 'group_drawing':init_group_drawing, 'group_hidden':init_group_hidden, 'group_title':init_group_title, 'group_description':init_group_description, 'group_access':init_group_access, 'group_privacy':init_group_privacy, 'group_taggers':init_group_taggers})
			context['form'] = form

			return render(request, 'video/social_group_settings.html', context)
		else:
			return HttpResponse("Somethings wrong here, but you are a member")
	init_group_moderation = group.group_moderation
	init_group_access = group.group_access
	init_group_privacy = group.group_privacy
	init_group_taggers = group.group_taggers
	init_group_title = group.group_title
	init_group_description = group.group_description
	init_group_hidden = group.group_hidden
	init_group_drawing = group.group_drawing
	form = GroupOptionsForm(initial={'group_moderation':init_group_moderation ,'group_drawing':init_group_drawing, 'group_hidden':init_group_hidden, 'group_title':init_group_title, 'group_description':init_group_description, 'group_access':init_group_access, 'group_privacy':init_group_privacy, 'group_taggers':init_group_taggers})
	context['form'] = form
	context.update(csrf(request))
	return render(request, 'video/social_group_settings.html', context)




def social_group(request, social_group_id):
	number = str(social_group_id)
	group = get_object_or_404(SocialGroup, pk = social_group_id)
	videos  = Vid.objects.filter(group_video = group)[:6]
	members = User.objects.filter(group_member = group, membership__membership_status = 2)[:6]
	admins = User.objects.filter(group_member = group, membership__membership_status = 6)[:6]
	requested = User.objects.filter(group_member = group, membership__membership_status = 1)
	comments = Comment.objects.filter(comment_group = group).prefetch_related('parent_comment').all()
	unmoderated_tags = Tag.objects.filter(group_tags = group, tag_moderation = 1)


	collections = Collection.objects.filter(collection_groups = group)[:6]
	slides = GroupSlide.objects.filter(slide_group = group)[:6]
	tags = Tag.objects.filter(group_tags = group)[:6]
	# check current users relationship to this group 
	# not currently working because I need to only check the membership status is one already exist...
	if request.user.is_authenticated():
		try:
			user_membership = Membership.objects.get(group = group, member = request.user)
			user_status = user_membership.membership_status
		except:
			user_status = 5	#5 offers the chance to login despite already having a membership

	else:
		user_status = 8 # not logged in

	context = {'admins':admins, 'collections':collections, 'slides':slides, 'tags':tags, 'unmoderated_tags':unmoderated_tags, 'comments':comments, 'number':number, 'videos':videos, 'group':group, 'members':members, 'requested':requested, 'user_status':user_status}
	
	
	return render(request, 'video/social_group.html', context)


def social_group_members(request, social_group_id):
	number = str(social_group_id)
	group = get_object_or_404(SocialGroup, pk = social_group_id)
	members = User.objects.filter(group_member = group, membership__membership_status = 2)[:6]
	admins = User.objects.filter(group_member = group, membership__membership_status = 6)[:6]
	requested = User.objects.filter(group_member = group, membership__membership_status = 1)
	comments = Comment.objects.filter(comment_group = group).prefetch_related('parent_comment').all()
	unmoderated_tags = Tag.objects.filter(group_tags = group, tag_moderation = 1)
	# check current users relationship to this group 
	# not currently working because I need to only check the membership status is one already exist...
	if request.user.is_authenticated():
		try:
			user_membership = Membership.objects.get(group = group, member = request.user)
			user_status = user_membership.membership_status
		except:
			user_status = 5	#5 offers the chance to login despite already having a membership

	else:
		user_status = 8 # not logged in

	context = {'admins':admins, 'unmoderated_tags':unmoderated_tags, 'comments':comments, 'number':number, 'group':group, 'members':members, 'requested':requested, 'user_status':user_status}
	
	
	return render(request, 'video/social_group_members.html', context)



def social_group_slides(request, social_group_id):
	number = str(social_group_id)
	group = get_object_or_404(SocialGroup, pk = social_group_id)
	videos  = Vid.objects.filter(group_video = group)
	members = User.objects.filter(group_member = group, membership__membership_status = 2)
	requested = User.objects.filter(group_member = group, membership__membership_status = 1)
	slides  = GroupSlide.objects.filter(slide_group = group)
	
	# check current users relationship to this group 
	# not currently working because I need to only check the membership status is one already exist...
	if request.user.is_authenticated():
		user = request.user
		try:
			user_membership = Membership.objects.get(group = group, member = user)
			user_status = user_membership.membership_status
			if user_status == 2 or user_status == 6:#and whatever admin is...
				user_slides = GroupSlide.objects.filter(slide_creator = user).exclude(slide_group = group)

		except:
			user_status = 5	#5 offers the chance to login despite already having a membership

	else:
		user_status = 8 # not logged in

	args = {'number':number, 'videos':videos, 'group':group, 'members':members, 'requested':requested, 'user_status':user_status, 'slides':slides}

	if user_slides:
		args['user_slides'] = user_slides

	if request.POST:
		form = SlideForm(request.POST, request.FILES)
		if form.is_valid():
			slide_name = form.cleaned_data['slide_name']
			slide_image = form.cleaned_data['slide_image']
			user = request.user
			new_slide = GroupSlide(slide_creator = user, slide_name = slide_name, slide_image = slide_image, slide_group = group)
			new_slide.save()

	
			return HttpResponseRedirect('/video/social_group/%s/slides' % (group.id))

		else:
			return HttpResponse("Aomethings wrong here")	
	else:
		form = SlideForm(request.POST)
		#args = {}
		args.update(csrf(request))
		args['form'] = form
		return render(request, 'video/social_group_slides.html', args)



def tag_page(request, social_group_id, tag_id):
	user = request.user
	tag = get_object_or_404(Tag, pk = tag_id)
	video = tag.video
	group = get_object_or_404(SocialGroup, pk = social_group_id)
	slides  = GroupSlide.objects.filter(slide_group = group)
	comments = Comment.objects.filter(comment_tag = tag).prefetch_related('parent_comment').all()
	collections = Collection.objects.filter(collection_creator = user)
	#slide_id = tag.tag_slide.id
	#slide = get_object_or_404(GroupSlide, pk = slide_id)

	if request.POST:
		form = EditTagForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			old_slide_id = form.cleaned_data['old_slide']
			slide_id = form.cleaned_data['slide']
			tag.tag_title = title
			tag.tag_description = description
			
			
			if slide_id > 0:
				new_slide = get_object_or_404(GroupSlide, pk = slide_id)
				if old_slide_id > 0:
					old_slide = get_object_or_404(GroupSlide, pk = old_slide_id)
					tag.tag_slide.remove(old_slide)	
				tag.tag_slide.add(new_slide)
			tag.save()
					#return the page
			return HttpResponseRedirect('/video/social_group/%s/%s/tag' %(social_group_id ,tag_id)) # need to pass a message here that tag was changed

		else:	
			return HttpResponse("Aomethings wrong here on the tag page form thing")

	else:
		form = EditTagForm()	
		args = {'tag':tag, 'video':video, 'group':group, 'slides':slides, 'form':form, 'comments':comments, 'collections':collections }		

		return render(request, 'video/tag.html', args)






''' commented because we no longer use this form - we use ajax
	if request.POST:	
		form = FormVideoSelectFilter(request.POST, instance = group)
		if form.is_valid():
			form.save()

			return HttpResponse("Groups added")
		else:
			return HttpResponse("Aomethings wrong here")	
	else:
		form = FormVideoSelectFilter(instance = group)
		args = {}
		context.update(csrf(request))
		context['form'] = form
		
		return render(request, 'video/social_group.html', context)
'''
''' commented because we no longer use this form - we use ajax
def social_group_save(request):
	number = request.POST['number']
	group = get_object_or_404(SocialGroup, pk = number)

	if request.POST:	
		form = FormVideoSelect(request.POST, instance = group)
		if form.is_valid():
			form.save()

			return HttpResponse("Videos added")
		else:
			return HttpResponse("Aomethings wrong here")
'''

#view for ajax video search / filter
def video_search(request, social_group_id):
	group = SocialGroup.objects.get(pk = social_group_id)
	if request.POST:	
		search_text = request.POST["search_text"]
	else:
		search_text = ""

	videos = Vid.objects.filter(video_title__contains = search_text).exclude(group_video = group).exclude(private = True)

	return render_to_response('video/ajax_video_search.html', {'videos':videos})

#view for ajax group search / filter
def group_search(request, user_profile_id):
	#group = SocialGroup.objects.get(pk = social_group_id)
	if request.POST:	
		search_text = request.POST["search_text"]
	else:
		search_text = ""

	user = request.user
	#list groups but remove the ones the user is already a mmber of
	groups = SocialGroup.objects.filter(group_title__contains = search_text).exclude(group_access = 3)

	return render_to_response('video/ajax_group_search.html', {'groups':groups})	

#view for ajax user search / filter
def user_search(request, social_group_id):
	if request.POST:	
		search_text = request.POST["search_text"]
	else:
		search_text = ""
	group = get_object_or_404(SocialGroup, pk = social_group_id)
#exclude list of users who are already members - already requested - already invited - already rejected invitation 
 #users previously rejected can still invited
	users = User.objects.exclude(Q(membership__group = group) & ~Q(membership__membership_status = 3)).filter(username__contains = search_text)[:10]

	return render_to_response('video/ajax_user_search.html', {'users':users})	

def collect_tag_page(request, social_group_id, tag_id):
	if request.POST:
		collection_id = request.POST.get('collection')
		tag_id = request.POST.get('tag')
		collection = get_object_or_404(Collection, pk = collection_id)
		tag = get_object_or_404(Tag, pk = tag_id)
		collection.collection_tags.add(tag)

		response_data = {}
		return HttpResponse(
			json.dumps(response_data),
			content_type = "application/json"
			)
	else:
		return HttpResponse("Aomethings wrong here")

def link_video_group(request, social_group_id):
	if request.POST:
		video_id = request.POST.get('video_id')
		video = get_object_or_404(Vid, pk = video_id)
		group = get_object_or_404(SocialGroup, pk = social_group_id)
		

		group.group_video.add(video)

		response_data = {}

		response_data['result'] = 'Create tag successful!'
		response_data['video_pk'] = video.pk
		response_data['video_title'] = video.video_title


		return HttpResponse(
			json.dumps(response_data),
			content_type = "application/json"
			)

	else:
		return HttpResponse("Aomethings wrong here")



#def SelectVideos(request, b = None):
#	instance = None
#	if b is not None:
#		instance = SocialGroup.objects.get(group_title = b)
#	#group_for_vids = SocialGroup.objects.get(pk = 1)
#	if request.POST:	
#		form = FormVideoSelect(request.POST, instance = instance)
#		if form.is_valid():
#			form.save()
#
#			return HttpResponse("Groups added")
#		else:
#			return HttpResponse("Aomethings wrong here")	
#	else:
#		return render_to_response('video/select_group.html/')


#class FormGroupSelect(ModelForm):
#	class Meta:
#        model = SocialGroup
#        fields = ('group_videos',)
#
#	choices = forms.ModelMultipleChoiceField(queryset = SocialGroup.objects.all, required = False, widget = FilteredSelectMultiple('group_videos', False),)
#
#def SelectGroups(request, vid_id):
#	video_to_group = Vid.objects.get(pk = vid_id)
#	#form = FormGroupSelect(SocialGroup.objects.all(), request.POST)
#	if request.POST:	
#		if form.is_valid():
#			form = FormGroupSelect(request.POST)
#			choices = form.cleaned_data['choices']
#			video_to_group.update(SocialGroup.group_video.through = choices)
#			return HttpResponse("Groups added")
#		else:
#			return HttpResponse("Aomethings wrong here")	
#	else:
#		return render_to_response('video/select_group.html/')


class Form_tag_delete(forms.Form):
	#we are creating a form so that we can use django validators to check what is being sent - nothing malicous
	tag = forms.IntegerField()
@csrf_exempt # probably need to pull this delete stuff into another view so this csrf isn't an issue

def delete_tag(request, vid_id):
	return_value = 0
	
	form = Form_tag_delete(request.POST)
	if form.is_valid():
		id_tag = form.cleaned_data ['tag']
		tag_record = Tag.objects.get(id=id_tag)
		tag_record.delete()
		return_value = id_tag

	return HttpResponse(json.dumps(return_value),content_type = "application/json")


class Form_slide_delete(forms.Form):
	#we are creating a form so that we can use django validators to check what is being sent - nothing malicous
	slide = forms.IntegerField()
@csrf_exempt # probably need to pull this delete stuff into another view so this csrf isn't an issue

def delete_slide(request, social_group_id):
	return_value = 0
	
	form = Form_slide_delete(request.POST)
	if form.is_valid():
		id_slide = form.cleaned_data ['slide']
		slide_record = GroupSlide.objects.get(id=id_slide)
		slide_record.delete()
		return_value = id_slide

	return HttpResponse(json.dumps(return_value),content_type = "application/json")

# accept / decline membership request 
def confirm_member(request, social_group_id):
	if request.method == "POST":
		member = request.POST.get('member')
		response = request.POST.get('response')
		this_member = get_object_or_404(User, pk = member)
		this_group = get_object_or_404(SocialGroup, pk = social_group_id)

		membership = Membership.objects.get(group = this_group, member = this_member)
		membership.membership_status = response
		membership.save()

		return HttpResponse(json.dumps(this_group.id),"It saves okay... maybe")
	else:
		return HttpResponse("Aomethings wrong here")

##accept / reject moderation on tag
def respond_moderation(request, social_group_id):
	if request.method == "POST":
		tag = request.POST.get('tag')
		response = request.POST.get('response')
		tag = get_object_or_404(Tag, pk = tag)
		tag.tag_moderation = response
		tag.save()
		return HttpResponse("It saves okay... maybe")
	else:
		return HttpResponse("Aomethings wrong here")


# accept / decline group invitations
def respond_invitation(request, user_profile_id):
	if request.method == "POST":
		group = request.POST.get('group')
		response = request.POST.get('response')
		this_member = get_object_or_404(User, pk = user_profile_id)
		this_group = get_object_or_404(SocialGroup, pk = group)

		membership = Membership.objects.get(group = this_group, member = this_member)
		membership.membership_status = response
		membership.save()

		return HttpResponse("It saves okay... maybe")
	else:
		return HttpResponse("Aomethings wrong here")

# invite a user to a group
def user_invite(request, social_group_id):
	if request.method == "POST":
		#group = request.POST.get('group')
		member = request.POST.get('member')
		status = request.POST.get('response')
		inv_group = get_object_or_404(SocialGroup, pk = social_group_id)
		inv_user = get_object_or_404(User, pk = member)
		#status = 4 # status invited


		#sending email notification "You have been invited..." - first attempt
		#send_mail(subject, message, from_email, to_list, fail_silently = True)
		subject = 'TagFrame: Invitation to a group'
		message = 'You have been invited to join the group' + inv_group.group_title
		from_email = settings.EMAIL_HOST_USER
		to_list = [inv_user.email, settings.EMAIL_HOST_USER]

		#check if the membership already exists
		#count_memberships = Membership.objects.filter(group = inv_group, member = inv_user).count()
		if Membership.objects.filter(group = inv_group, member = inv_user).exists():
			m1 = Membership.objects.get(group = inv_group, member = inv_user)
			m1.membership_status = status
			m1.save()
			send_mail(subject, message, from_email, to_list, fail_silently=False)

		else:
			m1 = Membership.objects.create(group = inv_group, member = inv_user, membership_status = 4)
			send_mail(subject, message, from_email, to_list, fail_silently=False)

		response_data = {}
		response_data['user_avatar'] = inv_user.userprofile.avatar.name
		response_data['user_name'] = inv_user.username
		response_data['user_id'] = inv_user.id

		return HttpResponse(
			json.dumps(response_data),
			content_type = "application/json"
			)


	else:
		return HttpResponse("Aomethings wrong here")
	#membership_name = user + group_video
	#user = User.objects.get(pk = user)
	#social_group = SocialGroup.objects.get(pk = social_group)
	#status = 1

#request from a user to join a group
# if groups is set to invite only (3) we need to deny this and hide it in the frontend
# if its set to (1)-anyone can join - we can just

def request_group(request, social_group_id):
	if request.method == "POST":
		group = request.POST.get('group')
		user = request.POST.get('user')

		req_group = SocialGroup.objects.get(pk = group)
		req_user = User.objects.get(pk = user)

		if req_group.group_access == 1: # anyone can join - set to member
			m1 = Membership.objects.create(group = req_group, member = req_user, membership_status = 2)

		if req_group.group_access == 2: #set to requested
			m1 = Membership.objects.create(group = req_group, member = req_user, membership_status = 1)

		response_data = {}	

		return HttpResponse(
				json.dumps(response_data),
				content_type = "application/json"
				)	

		
	else:
		return HttpResponse("Aomethings wrong here")
	#membership_name = user + group_video
	#user = User.objects.get(pk = user)
	#social_group = SocialGroup.objects.get(pk = social_group)
	#status = 1

def connect_user_slides(request, social_group_id):
	if request.method == "POST":
		group = request.POST.get('group')
		slide = request.POST.get('slide')
		
		this_slide = get_object_or_404(GroupSlide, pk= slide)
		this_group = get_object_or_404(SocialGroup, pk= group)
		this_slide.slide_group = this_group
		this_slide.save()
		response_data = {}	

		return HttpResponse(
				json.dumps(response_data),
				content_type = "application/json"
				)	

		
	else:
		return HttpResponse("Aomethings wrong here")

def create_tag(request, vid_id, tag_time = None, social_group_id = None):

	video_to_link = Vid.objects.get(pk = vid_id)
	#dataUrlPattern = re.compile('data:image/png;base64,(.*)$')
	user_profile = request.user

	#is this a genuine member of the group or have they changed the css? 
	#still need to confirm what status - 
	#needs to be 2 or 6 to be abke to tag


# video_to_link = str(vid_id)
	if request.method == "POST":
		slide_id = request.POST.get('slide_id')
		tag_title = request.POST.get('tag_title')
		tag_start = request.POST.get('tag_start')
		tag_description = request.POST.get('tag_description')
		tag_start_string = request.POST.get('tag_start_string')
		tag_image = request.POST.get('tag_image')
		tag_draw = request.POST.get('tag_draw')
		time_secs = request.POST.get('time_secs')
		cur_group_number = request.POST.get('cur_group')
		cur_group_number_int = int(cur_group_number)
		slide_id_int = int(slide_id)
		#if cur_group_number is None:
		#	cur_group_number = 0
		group = get_object_or_404(SocialGroup, pk = cur_group_number_int)
		if Membership.objects.filter(member = user_profile, group = cur_group_number, membership_status = 2).exists():
			group_member = True
		else: 
			group_member = False	
		if Membership.objects.filter(member = user_profile, group = cur_group_number, membership_status = 6).exists():
			group_manager = True
		else: 
			group_manager = False
		response_data = {}

		if group_member == True and group.group_taggers == 1 or \
			group_manager == True:
			member_of_group = True

			#members could still tag on groups with taggers set to managers only if they bypass the css
			## if group_taggers is set to 2 - user must be a manager to tag (6 = manager  - 2 = accepted)


		#image_data = base64.b64decode(tag_draw)

			if tag_image.startswith("data:image/jpeg;base64,"): #Currently tag image cant be created from youtube so need the "if"
				tag_image = tag_image[22:]
				tag_image = base64.b64decode(tag_image)
				tag_image_file = ContentFile(tag_image, 'tag.jpg')
				isimage = True

			else:
				isimage = False	
			#else:
			#	tag_image_file = "blank- fucking youtube"

			if tag_draw.startswith("data:image/png;base64,"):
				isdrawing = True
				tag_draw = tag_draw[22:]
				tag_draw = base64.b64decode(tag_draw)
				tag_draw_file = ContentFile(tag_draw, 'draw.png')
				if group.group_drawing == 1 and group_manager == False: #if draw status is limited to managers only and the user is not a manager
					return HttpResponse("You really shouldnt be allowed to draw on this group")

			else:
				isdrawing = False

			if isimage is False and isdrawing is False:
				tag = Tag(user = user_profile, time_secs = time_secs, video = video_to_link, tag_title = tag_title, tag_description = tag_description, tag_start_string = tag_start_string, tag_start = tag_start)			

			if isimage is False and isdrawing is True:	
				tag = Tag(tag_draw = tag_draw_file, user = user_profile, time_secs = time_secs, video = video_to_link, tag_title = tag_title, tag_description = tag_description, tag_start_string = tag_start_string, tag_start = tag_start)
			

			if isimage is True and isdrawing is True:	
				tag = Tag(tag_image = tag_image_file, tag_draw = tag_draw_file, user = user_profile, time_secs = time_secs, video = video_to_link, tag_title = tag_title, tag_description = tag_description, tag_start_string = tag_start_string, tag_start = tag_start)
			
			if isimage is True and isdrawing is False:	
				tag = Tag(tag_image = tag_image_file, user = user_profile, time_secs = time_secs, video = video_to_link, tag_title = tag_title, tag_description = tag_description, tag_start_string = tag_start_string, tag_start = tag_start)
			tag.save()
			cur_group = get_object_or_404(SocialGroup, pk = cur_group_number_int)
			if cur_group.group_moderation == 1: #no moderation is required
				tag.tag_moderation = 2 #tag is approved automatically
			else:
				tag.tag_moderation = 1 #tag is unmoderated

			tag.save()
			cur_group.tag_groups.add(tag)

			if slide_id_int > 0:
				slide_object = get_object_or_404(GroupSlide, pk = slide_id)		
				tag.tag_slide.add(slide_object)

			#tag = Tag(tag_draw = tag_draw_file, user = user_profile, time_secs = time_secs, video = video_to_link, tag_title = tag_title, tag_description = tag_description, tag_start_string = tag_start_string, tag_start = tag_start, tag_image = "nada")

			def encode_image(obj):
				if isinstance(obj, tag_image):
					return obj.path	

			response_data['result'] = 'Create tag successful!'
			response_data['tagpk'] = tag.pk
			response_data['tag_title'] = tag.tag_title
			response_data['time_secs'] = tag.time_secs
			response_data['tag_description'] = tag.tag_description
			response_data['tag_user_id'] = tag.user.id
			response_data['user_avatar'] = tag.user.userprofile.avatar.name
			if isimage is True:
				response_data['tag_image'] = tag.tag_image.name
			if slide_id_int > 0:
				response_data['slide_image'] = slide_object.slide_image.name		
			response_data['tag_start_string'] = tag.tag_start_string
			response_data['tag_start'] = tag.tag_start
			response_data['tag_user_email'] = tag.user.email
			response_data['tag_username'] = tag.user.username
			response_data['tag_group'] = cur_group_number

			if tag.tag_draw:
				response_data['tag_draw'] = tag.tag_draw.name

			return HttpResponse(
				json.dumps(response_data),
				content_type = "application/json"
				)
			
		else:
			return HttpResponse("You seem not to be a member of this group")
			

	else:
		member_of_group = False		
		return HttpResponse("Somethings wrong here, but you are a member")

#create saves a poster image when the video is uploaded - potentially also if they want to change it later
def create_poster(request, vid_id, tag_time, social_group_id):

	video_to_link = Vid.objects.get(pk = vid_id)
	user_profile = request.user

# video_to_link = str(vid_id)
	if request.method == "POST":
		
		tag_image = request.POST.get('tag_image')
		response_data = {}
		if tag_image.startswith("data:image/jpeg;base64,"): #Currently tag image cant be created from youtube so need the "if"
			tag_image = tag_image[22:]	
			tag_image = base64.b64decode(tag_image)
			tag_image_file = ContentFile(tag_image, 'tag.jpg')

			def encode_image(obj):
				if isinstance(obj, tag_image):
					return obj.path	

			video_to_link.poster = tag_image_file
			video_to_link.save()

			response_data['result'] = 'Create tag successful!'


			return HttpResponse(
				json.dumps(response_data),
				content_type = "application/json"
				)
			
		else:
			return HttpResponse("Somethings wrong here, but you are a member")

	else:
		member_of_group = False		
		return HttpResponse("Whoa  what do you think you're playing at?!")


