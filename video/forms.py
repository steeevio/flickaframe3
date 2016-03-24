from django import forms
from video.models import Vid, Tag, SocialGroup, GroupSlide

#class UploadForm(forms.ModelForm):
#	class Meta:
#		model = Vid
#		fields = ('video_title', 'youtube_id','video_file', 'poster_time', 'video_description' )
#		widgets = {'poster_time': forms.HiddenInput()}

class UploadForm(forms.Form):
	video_title = forms.CharField(label="Video title", max_length = 140)
	youtube_id = forms.CharField(label="Youtube Url", required = False)
	video_description = forms.CharField(label="Video description", max_length = 250, required=False)
	video_file = forms.FileField(label="Video File", required=False)
	private = forms.BooleanField(label="Video private", required=False)
	poster_time = forms.IntegerField(required=False)

class EditTagForm(forms.Form):
	old_slide = forms.IntegerField(label="old_slide id")
	slide = forms.IntegerField(label="slide id")
	title = forms.CharField(label="Title", max_length = 300)
	description = forms.CharField(label="description")


class GroupOptionsForm(forms.Form):
	ACCESSCHOICES = (('1', 'Anyone',), ('2', 'Approved Only',), ('3', 'Invited Only',))
	PRIVACYCHOICES = (('1', 'Anyone',), ('2', 'Members Only',))
	TAGGERSCHOICES = (('1', 'Anyone',), ('2', 'Members Only',))
	HIDDENCHOICES = (('1', 'Show Group',), ('2', 'Hide Group',))
	DRAWINGCHOICES = (('1', 'Managers Only',), ('2', 'All Members',))
	MODERATIONCHOICES = (('1', 'No Moderation',), ('2', 'Moderation Required',))	
	group_access = forms.ChoiceField(widget=forms.RadioSelect(), choices=ACCESSCHOICES)
	group_privacy = forms.ChoiceField(widget=forms.RadioSelect(), choices=PRIVACYCHOICES)
	group_taggers = forms.ChoiceField(widget=forms.RadioSelect(), choices=TAGGERSCHOICES)
	group_hidden = forms.ChoiceField(widget=forms.RadioSelect(), choices=HIDDENCHOICES)
	group_drawing = forms.ChoiceField(widget=forms.RadioSelect(), choices=DRAWINGCHOICES)
	group_moderation = forms.ChoiceField(widget=forms.RadioSelect(), choices=MODERATIONCHOICES)
	group_title = forms.CharField(label="Title", max_length = 300)
	group_description = forms.CharField(label="description", max_length = 800)
		

class SlideForm(forms.ModelForm):
	class Meta:
		model = GroupSlide
		fields = ('slide_name', 'slide_image' )
		widgets = {
			'slide_image': forms.FileInput(attrs = {

				'onchange': "upload_img(this);"
			}
				),

					}



class TagForm(forms.ModelForm):
	class Meta:

		model = Tag
		fields = ('tag_title', )
		widgets = {

			'tag_title':forms.TextInput(
			attrs = {'id':'tag_title', 'required':True, 'placeholder':'Write a damn tag'}
			),
						

			
				}			

class GroupForm(forms.Form):

	group_title = forms.CharField(label="Group title", max_length = 140)
	group_description = forms.CharField(label="Video description", max_length = 250, required=False)
	group_images = forms.FileField(label="Group Header Image", required=False)
	add_video = forms.IntegerField(required=False)

class CollectionForm(forms.Form):

	collection_name = forms.CharField(label="Collection title", max_length = 140)
	collection_description = forms.CharField(label="Collection description", max_length = 1000, required=False)
	collection_tag = forms.IntegerField(required=False)	



	#class Meta:
	#	model = SocialGroup
	#	fields = ('group_title', 'group_description', 'group_images')



	#	widgets = {
	#		'group_images': forms.FileInput(attrs = {

	#			'onchange': "upload_img(this);"
	#		}
#				),
#
#					}
			