from django.shortcuts import render
from django.http import HttpResponse

from django import forms
#import django forms package

class Form_inscription(forms.Form):
	video_title = forms.CharField(label="Video Title", max_length=200)
	video_description = forms.CharField(label="Video description", max_length=500)
	user = forms.ModelChoiceField(label = "Video Creator", queryset = User.objects.all())

#Create view for upload video
def page(request):
	if request.POST:
		form = Form_inscription(request.POST)
		#if the form has been posted, we create the variable that will contain out form filled with data from the POST form
		if form.is_valid():
			# checks if data is consistent with the fields defined in the form	
			video_title = form.cleaned_data['video_title']
			video_description = form.cleaned_data['video_description']
			user = form.cleaned_data['user']
			new_video = Vid(video_title = video_title, video_description = video_description)
			new_video.save()
			return HttpResponse("Video added")

		else:
			return render(request, '/upload.html/')