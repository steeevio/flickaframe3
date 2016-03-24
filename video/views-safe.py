from django.shortcuts import get_object_or_404, render, render_to_response
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import CheckboxSelectMultiple
from easy_thumbnails.files import get_thumbnailer
from django.core.files.base import ContentFile
from itertools import chain

from django.db.models import Q




from.models import Vid, Tag, UserProfile, Comment, SocialGroup, GroupSlide, Membership, get_upload_draw_image_name, get_upload_avatar_name
from django import forms
from video.forms import UploadForm
from video.forms import GroupForm
from video.forms import EditTagForm
from video.forms import SlideForm
from video.forms import GroupOptionsForm
from django import forms
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login #import neccesary function for login authentication
from django.contrib.auth import logout
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
	video_list = Vid.objects.order_by('-pub_date')[:10]
	user_list = User.objects.order_by('id')[:10]
	group_list = SocialGroup.objects.order_by('id')[:10]
	context = {'video_list': video_list, 'user_list':user_list, 'group_list':group_list}
	return render(request, 'video/index.html', context)


def log_out(request):
	logout(request)
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
def create_group(request):
	if request.POST:
		form = GroupForm(request.POST, request.FILES)
		if form.is_valid():
			group_title = form.cleaned_data['group_title']
			group_description = form.cleaned_data['group_description']
			group_image = form.cleaned_data['group_images']
			group_owner = request.user
			new_group = SocialGroup(group_description = group_description, group_owner = group_owner, group_title = group_title, group_images = group_image)

			new_group.save()
			m1 = Membership.objects.create(group = new_group, member = group_owner, membership_status = 6, manager = True)
			return HttpResponseRedirect("/video/social_group/%s/" % new_group.id)
		else:
			return HttpResponse("Aomethings wrong here")	


	else:
		form = GroupForm(request.POST)
		args = {}
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
	videos  = Vid.objects.filter(user = user_profile)
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

	context = {'test_current_user':test_current_user, 'test_profile_user':test_profile_user, 'videos': videos, 'user_profile':user_profile, 'groups':groups, 'tags':tags, 'number':number, 'this_user':this_user, 'group_invites':group_invites,}

	return render(request, 'video/user_profile.html', context)	
''' not user anymore - no longer have a form on the page to select groups we now do this on the groups pages only
	if request.POST:	
		form = FormUserSelectGroup(request.POST, instance = user_profile)
		if form.is_valid():
			form.save()

			return HttpResponse("Groups added")
		else:
			return HttpResponse("Aomethings wrong here")	
	else:
		form = FormUserSelectGroup(instance = user_profile)
		args = {}
		context.update(csrf(request))
		context['form'] = form
'''		
		


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


#def upload(request):
	#return render(request, 'video/upload.html')

#view for a video at a specific time
def video_time_specific(request, vid_id, tag_time):
	number = str(vid_id)
	tag_time = str(tag_time)
	video = get_object_or_404(Vid, pk = vid_id)
	tags = Tag.objects.filter(video = video) # exclude tags that are part of a group that has a group_privacy status of 2
	group = video.base_group
	groups = SocialGroup.objects.filter(group_video = video)
	tags = tags.prefetch_related('tag_slide').all()
	comments = Comment.objects.filter(comment_video = video).prefetch_related('parent_comment').all()

	if request.user.is_authenticated():
		user = request.user
		groups_accepted = SocialGroup.objects.filter(group_video = video, group_member = user, membership__membership_status = 2)
		groups_manager = SocialGroup.objects.filter(group_video = video, group_member = user, membership__membership_status = 6)
		groups_member =  list(chain(groups_accepted, groups_manager))
		not_groups_member = SocialGroup.objects.filter(group_video = video).exclude(group_member = user)
		slides = GroupSlide.objects.filter(slide_group__in = groups_member)
	else:
		user = None
		groups_member= None
		not_groups_member = SocialGroup.objects.filter(group_video = video)
		slides = None

	context = {'coments':comments, 'slides':slides, 'user':user, 'number': number, 'video':video, 'tags':tags, 'group':group, 'groups':groups, 'tag_time':tag_time, 'groups_member':groups_member, 'not_groups_member':not_groups_member}
	
	data = Tag.objects.values_list('tag_start','tag_title')
	#data_json = json.dumps(list(data), cls=DjangoJSONEncoder)
	#data = Tag.objects.values('tag_start')[0]
	return render(request, 'video/video.html', context)


# video view coming from a specific group - passes script to show only group tags
def video_group_specific(request, vid_id, social_group_id):


	group = get_object_or_404(SocialGroup, pk = social_group_id)
	number = str(vid_id)
	video = get_object_or_404(Vid, pk = vid_id)
	tags = Tag.objects.filter(video=video)
	groups = SocialGroup.objects.filter(group_video = video)
	tags = tags.prefetch_related('tag_slide').all()
	comments = Comment.objects.filter(comment_video = video).prefetch_related('parent_comment').all()

	if request.user.is_authenticated():
		user = request.user
		#groups_member = SocialGroup.objects.filter(group_video = video, group_member = user)

		groups_accepted = SocialGroup.objects.filter(group_video = video, group_member = user, membership__membership_status = 2)
		groups_manager = SocialGroup.objects.filter(group_video = video, group_member = user, membership__membership_status = 6)
		groups_member =  list(chain(groups_accepted, groups_manager))

		not_groups_member = SocialGroup.objects.filter(group_video = video).exclude(group_member = user)
		slides = GroupSlide.objects.filter(slide_group__in = groups_member)
		
		if Membership.objects.filter(member = user, group = group).exists():
			member_of_group = True
		else:
			member_of_group = False
	else:
		user = None
		groups_member = None
		not_groups_member = SocialGroup.objects.filter(group_video = video)
		member_of_group = False
		slides = None

	context = {'comments':comments, 'slides':slides, 'member_of_group':member_of_group, 'user':user, 'number': number, 'video':video, 'tags':tags, 'group':group, 'groups':groups, 'groups_member':groups_member, 'not_groups_member':not_groups_member}
	
	data = Tag.objects.values_list('tag_start','tag_title')
	#data_json = json.dumps(list(data), cls=DjangoJSONEncoder)
	#data = Tag.objects.values('tag_start')[0]
	return render(request, 'video/video.html', context)

#view for a video
def video(request, vid_id):
	number = str(vid_id)
	video = get_object_or_404(Vid, pk = vid_id)
	tags = Tag.objects.filter(video=video)
	group = video.base_group
	groups = SocialGroup.objects.filter(group_video = video)
	tags = tags.prefetch_related('tag_slide').all()
	comments = Comment.objects.filter(comment_video = video).prefetch_related('parent_comment').all()



	if request.user.is_authenticated():
		user = request.user
		groups_accepted = SocialGroup.objects.filter(group_video = video, group_member = user, membership__membership_status = 2)
		groups_manager = SocialGroup.objects.filter(group_video = video, group_member = user, membership__membership_status = 6)
		groups_member =  list(chain(groups_accepted, groups_manager))
		not_groups_member = SocialGroup.objects.filter(group_video = video).exclude(group_member = user)
		##I want this to provide all of the slides relevant to the current group displaying if I am a member
		slides = GroupSlide.objects.filter(slide_group__in = groups_member)
	else:
		user = None
		groups_member= None
		not_groups_member = SocialGroup.objects.filter(group_video = video)
		slides = None

	context = {'comments':comments, 'slides':slides, 'user':user, 'number': number, 'video':video, 'tags':tags,'group':group, 'groups':groups, 'groups_member':groups_member, 'not_groups_member':not_groups_member}
	
	data = Tag.objects.values_list('tag_start','tag_title')
	#data_json = json.dumps(list(data), cls=DjangoJSONEncoder)
	#data = Tag.objects.values('tag_start')[0]
	return render(request, 'video/video.html', context)
	#return HttpResponse(json.dumps(data), content_type='application/json')

#view for the initial video after upload that takes a screenshot -need to integrate these views
def video_initial(request, vid_id, social_group_id, poster_time_str):

	group = get_object_or_404(SocialGroup, pk = social_group_id)
	number = str(vid_id)
	video = get_object_or_404(Vid, pk = vid_id)
	tags = Tag.objects.filter(video=video)
	groups = SocialGroup.objects.filter(group_video = video)
	script = "window.onload = setPoster(" + poster_time_str + "); "
	if request.user.is_authenticated():
		user = request.user
		#groups_member = SocialGroup.objects.filter(group_video = video, group_member = user)

		groups_accepted = SocialGroup.objects.filter(group_video = video, group_member = user, membership__membership_status = 2)
		groups_manager = SocialGroup.objects.filter(group_video = video, group_member = user, membership__membership_status = 6)
		groups_member =  list(chain(groups_accepted, groups_manager))

		not_groups_member = SocialGroup.objects.filter(group_video = video).exclude(group_member = user)
		slides = GroupSlide.objects.filter(slide_group__in = groups_member)
		
		if Membership.objects.filter(member = user, group = group).exists():
			member_of_group = True
		else:
			member_of_group = False
	else:
		user = None
		groups_member = None
		not_groups_member = SocialGroup.objects.filter(group_video = video)
		member_of_group = False

	context = {'script':script, 'member_of_group':member_of_group, 'user':user, 'number': number, 'video':video, 'tags':tags, 'group':group, 'groups':groups, 'groups_member':groups_member, 'not_groups_member':not_groups_member}
	
	data = Tag.objects.values_list('tag_start','tag_title')
	#data_json = json.dumps(list(data), cls=DjangoJSONEncoder)
	#data = Tag.objects.values('tag_start')[0]
	return render(request, 'video/video.html', context)




#	class Form_inscription(forms.Form):
#	video_title = forms.CharField(label="Video Title", max_length=200)
#	video_description = forms.CharField(label="Video description", max_length=500)
#	video_file = forms.FileField(label="video file")

#Create view for upload video
#def page(request):
#	if request.POST:
#		form = Form_inscription(request.POST, request.FILES)
		#if the form has been posted, we create the variable that will contain out form filled with data from the POST form
#		if form.is_valid():
		# checks if data is consistent with the fields defined in the form	
#			video_title = form.cleaned_data['video_title']
	#		video_description = form.cleaned_data['video_description']
	#		video_file = form.cleaned_data['video_file']
	#		user = User.objects.get(user=self.request.user)
	#		new_video = Vid(video_title = video_title, video_description = video_description, user = user)

	#		new_video.save()
	#		return HttpResponse("Video added")

#		else:
	#		return render(request, 'video/index.html/', {'form':form})
#	else:
#		form = Form_inscription()
	#	return render(request, 'video/upload.html/',{'form':form})		

#Create view for upload video using model

def upload_page(request):

	if request.POST:
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			video_title = form.cleaned_data['video_title']
			video_description = form.cleaned_data['video_description']
			video_file = form.cleaned_data['video_file']
			youtube_id = form.cleaned_data['youtube_id']

			poster_time = form.cleaned_data['poster_time']
			if poster_time:
				poster_time_str = str(poster_time)
			else:
				poster_time_str = "5"	
			
			if len(youtube_id) > 0:
				youtube_id = youtube_id.split("?v=")[1]
			user = request.user

			#create the video object
			new_video = Vid( youtube_id = youtube_id, video_title = video_title, video_description = video_description, user = user, video_file = video_file)
			new_video.save()

			# create a group linked to this new video
			base_group = SocialGroup(group_owner = user, group_title = "Base Group:" + video_title, group_description = "This is the base group for this video")
			base_group.save()
			base_group.group_video.add(new_video)

			m1 = Membership.objects.create(group = base_group, member = user, membership_status = 6)
			

			#link the base group as a foreign key so we know its the main group for this video - might be a better way to just use the first group for a video
			new_video.base_group = base_group
			new_video.save()
			if len(youtube_id) > 0:
				return HttpResponseRedirect('/video/%s/%s/from_group' % (new_video.id, base_group.id))
			else:
				return HttpResponseRedirect('/video/%s/%s/%s/init' % (new_video.id, base_group.id, poster_time_str))
				
				
					
			
		else:
			return HttpResponse("Aomethings wrong here")	
	else:
		form = UploadForm(request.POST)
		args = {}
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


def social_group(request, social_group_id):
	number = str(social_group_id)
	group = get_object_or_404(SocialGroup, pk = social_group_id)
	videos  = Vid.objects.filter(group_video = group)
	members = User.objects.filter(group_member = group, membership__membership_status = 2)
	requested = User.objects.filter(group_member = group, membership__membership_status = 1)
	comments = Comment.objects.filter(comment_group = group).prefetch_related('parent_comment').all()
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

	context = {'comments':comments, 'number':number, 'videos':videos, 'group':group, 'members':members, 'requested':requested, 'user_status':user_status}
	
	if request.POST:
		form = GroupOptionsForm(request.POST)
		if form.is_valid():
			group_access = form.cleaned_data['group_access']
			group_privacy = form.cleaned_data['group_privacy']
			group_taggers = form.cleaned_data['group_taggers']
			group_title = form.cleaned_data['group_title']
			group_description = form.cleaned_data['group_description']
			group.group_access = int(group_access)
			group.group_privacy = int(group_privacy)
			group.group_taggers = int(group_taggers)
			group.group_title = group_title
			group.group_description = group_description
			group.save()
			init_group_access = group.group_access
			init_group_privacy = group.group_privacy
			init_group_taggers = group.group_taggers
			init_group_title = group.group_title
			init_group_description = group.group_description	
			form = GroupOptionsForm(initial={'group_title':init_group_title, 'group_description':init_group_description, 'group_access':init_group_access, 'group_privacy':init_group_privacy, 'group_taggers':init_group_taggers})
			context['form'] = form

			return render(request, 'video/social_group.html', context)
		else:
			return HttpResponse("Somethings wrong here, but you are a member")
	init_group_access = group.group_access
	init_group_privacy = group.group_privacy
	init_group_taggers = group.group_taggers
	init_group_title = group.group_title
	init_group_description = group.group_description
	form = GroupOptionsForm(initial={'group_title':init_group_title, 'group_description':init_group_description, 'group_access':init_group_access, 'group_privacy':init_group_privacy, 'group_taggers':init_group_taggers})
	context['form'] = form
	context.update(csrf(request))
	return render(request, 'video/social_group.html', context)


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
		try:
			user_membership = Membership.objects.get(group = group, member = request.user)
			user_status = user_membership.membership_status
		except:
			user_status = 5	#5 offers the chance to login despite already having a membership

	else:
		user_status = 8 # not logged in

	args = {'number':number, 'videos':videos, 'group':group, 'members':members, 'requested':requested, 'user_status':user_status, 'slides':slides}

	if request.POST:
		form = SlideForm(request.POST, request.FILES)
		if form.is_valid():
			slide_name = form.cleaned_data['slide_name']
			slide_image = form.cleaned_data['slide_image']
			user = request.user
			new_slide = GroupSlide(slide_creator = user, slide_name=slide_name, slide_image = slide_image, slide_group = group)
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
	tag = get_object_or_404(Tag, pk = tag_id)
	video = tag.video
	group = get_object_or_404(SocialGroup, pk = social_group_id)
	slides  = GroupSlide.objects.filter(slide_group = group)
	comments = Comment.objects.filter(comment_tag = tag).prefetch_related('parent_comment').all()
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
		args = {'tag':tag, 'video':video, 'group':group, 'slides':slides, 'form':form, 'comments':comments}		

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

	videos = Vid.objects.filter(video_title__contains = search_text).exclude(group_video = group)

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
	groups = SocialGroup.objects.filter(group_title__contains = search_text)#.exclude(membership__member = user)

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

		#check if the membership already exists
		#count_memberships = Membership.objects.filter(group = inv_group, member = inv_user).count()
		if Membership.objects.filter(group = inv_group, member = inv_user).exists():
			m1 = Membership.objects.get(group = inv_group, member = inv_user)
			m1.membership_status = status
			m1.save()
		else:
			m1 = Membership.objects.create(group = inv_group, member = inv_user, membership_status = 4)

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
def request_group(request, social_group_id):
	if request.method == "POST":
		group = request.POST.get('group')
		user = request.POST.get('user')

		req_group = SocialGroup.objects.get(pk = group)
		req_user = User.objects.get(pk = user)

		status = 1

		m1 = Membership.objects.create(group = req_group, member = req_user, membership_status = 1)
		
		return HttpResponse("It saves okay... maybe")
	else:
		return HttpResponse("Aomethings wrong here")
	#membership_name = user + group_video
	#user = User.objects.get(pk = user)
	#social_group = SocialGroup.objects.get(pk = social_group)
	#status = 1

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

		
		response_data = {}

		if Membership.objects.filter(member = user_profile, group = cur_group_number, membership_status = 2).exists() or \
			Membership.objects.filter(member = user_profile, group = cur_group_number, membership_status = 6).exists():
			member_of_group = True

		#image_data = base64.b64decode(tag_draw)
		
		#dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
		#tag_draw = dataUrlPattern.match(tag_draw).group(2)
		# Decode the 64 bit string into 32 bit

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
			if cur_group_number_int > 0:
				cur_group = get_object_or_404(SocialGroup, pk = cur_group_number_int)
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
				response_data['tag_image'] = tag.tag_image.path
			if slide_id_int > 0:
				response_data['slide_image'] = slide_object.slide_image.path		
			response_data['tag_start_string'] = tag.tag_start_string
			response_data['tag_start'] = tag.tag_start
			response_data['tag_user_email'] = tag.user.email
			response_data['tag_username'] = tag.user.username
			response_data['tag_group'] = cur_group_number

			if tag.tag_draw:
				response_data['tag_draw'] = get_upload_draw_image_name(tag.tag_draw, "draw.png")

			return HttpResponse(
				json.dumps(response_data),
				content_type = "application/json"
				)
			
		else:
			return HttpResponse("Somethings wrong here, but you are a member")

	else:
		member_of_group = False		
		return HttpResponse("Whoa  what do you think you're playing at?!")

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


