from django.shortcuts import get_object_or_404, render, render_to_response
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf


from.models import Vid, Tag
from django import forms
from video.forms import UploadForm

import json

def index(request):
	video_list = Vid.objects.order_by('-pub_date')[:10]
	context = {'video_list': video_list}
	return render(request, 'video/index.html', context)

def upload(request):
	return render(request, 'video/upload.html')

def video(request, vid_id):
	number = str(vid_id)
	video = get_object_or_404(Vid, pk = vid_id)
	context = {'number': number, 'video':video}
	
	return render(request, 'video/video.html', context)

class Form_inscription(forms.Form):
	video_title = forms.CharField(label="Video Title", max_length=200)
	video_description = forms.CharField(label="Video description", max_length=500)
	video_file = forms.FileField(label="video file")

#Create view for upload video
def page(request):
	if request.POST:
		form = Form_inscription(request.POST, request.FILES)
		#if the form has been posted, we create the variable that will contain out form filled with data from the POST form
		if form.is_valid():
		# checks if data is consistent with the fields defined in the form	
			video_title = form.cleaned_data['video_title']
			video_description = form.cleaned_data['video_description']
			video_file = form.cleaned_data['video_file']
			new_video = Vid(video_title = video_title, video_description = video_description)
			new_video.save()
			return HttpResponse("Video added")

		else:
			return render(request, 'video/index.html/', {'form':form})
	else:
		form = Form_inscription()
		return render(request, 'video/upload.html/',{'form':form})		

#Create view for upload video using model

def upload_page(request):

	if request.POST:
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponse("Video added")
		else:
			return HttpResponse("Aomethings wrong here")	
	else:
		form = UploadForm(request.POST)
		args = {}
		args.update(csrf(request))
		args['form'] = form
		return render_to_response('video/upload.html/', args)

def create_tag(request, vid_id):

	video_to_link = Vid.objects.get( pk = vid_id)
	# video_to_link = str(vid_id)
	if request.method =="POST":
		tag_title = request.POST.get('tag_title')
		tag_start = request.POST.get('tag_start')
		tag_description = request.POST.get('tag_description')
		tag_start_string = request.POST.get('tag_start_string')
		tag_image = request.POST.get('tag_image')
		response_data = {}

		tag = Tag(video = video_to_link, tag_title = tag_title, tag_description = tag_description, tag_start_string = tag_start_string, tag_start = tag_start, tag_image = tag_image)
		tag.save()

		response_data['result'] = 'Create tag successful!'
		response_data['tagpk'] = tag.pk
		response_data['tag_title'] = tag.tag_title
		response_data['tag_description'] = tag.tag_description
		response_data['tag_image'] = tag.tag_image
		response_data['tag_start_string'] = tag.tag_start_string
		return HttpResponse(
			json.dumps(response_data),
			content_type = "application/json"
			)

		
		
	else:
		return HttpResponse("Aomethings wrong here")