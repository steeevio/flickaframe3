from django.conf.urls import url, include

from . import views

urlpatterns = [


#these urls really need turning round - so I can ditch most of them - 
# django reads from bottom up and matches the first key element then goes along looking for more specific
# i.e url(r'^create_tag/(?P<vid_id>[0-9]+)/$', views.create_tag, name='create_tag'),

	#attempt to implement the static.py to stop the byterange issue on chrome currentTime - not working :/
	#url(r'^static/video/uploadedfiles/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/video/uploadedfiles'}),

	url(r'^$', views.index, name='index'),
	url(r'^upload/$', views.upload_page, name='upload'),
	url(r'^create_group/$', views.create_group, name='create-group'),
	url(r'^create_group/(?P<vid_id>[0-9]+)/$', views.create_group, name='create-group-video'),

	url(r'^create_user/$', views.create_user_account, name='create'),
#	url(r'^select_group/$', views.select_group, name='select_group'),

	# create tag from URL
	url(r'^(?P<vid_id>[0-9]+)/create_tag/$', views.create_tag, name='create-tag'),
	# create tag from time
	url(r'^(?P<vid_id>[0-9]+)/(?P<tag_time>[0-9]+)/start/create_tag/$', views.create_tag, name='create-tag-from-time'),
	#create tag from group
	url(r'^(?P<vid_id>[0-9]+)/(?P<social_group_id>[0-9]+)/from_group/create_tag/$', views.create_tag, name='create-tag-from-group'),
	#create tag from group with time
	url(r'^(?P<vid_id>[0-9]+)/(?P<tag_time>[0-9]+)/(?P<social_group_id>[0-9]+)/start_group/create_tag/$', views.create_tag, name='create-tag-from-group-with-time'),
	#create tag on initial upload
	url(r'^(?P<vid_id>[0-9]+)/(?P<tag_time>[0-9]+)/(?P<social_group_id>[0-9]+)/init/create_tag/$', views.create_tag, name='create-tag-from-group-init'),
	#create poster on initial upload
	url(r'^(?P<vid_id>[0-9]+)/(?P<tag_time>[0-9]+)/(?P<social_group_id>[0-9]+)/init/create_poster/$', views.create_poster, name='create-tag-from-group-poster'),

	url(r'^(?P<vid_id>[0-9]+)/delete_tag/$', views.delete_tag, name='delete-tag'),
	url(r'^social_group/(?P<social_group_id>[0-9]+)/delete_slide/$', views.delete_slide, name='delete-slide'),	

	#accept/decline group
	url(r'^social_group/(?P<social_group_id>[0-9]+)/respond_moderation/$', views.respond_moderation, name='respond-to-moderation'),	

	# confirm / request membership
	url(r'^social_group/(?P<social_group_id>[0-9]+)/request_group/$', views.request_group, name='request-group'),
	url(r'^social_group/(?P<social_group_id>[0-9]+)/confirm_member/$', views.confirm_member, name='confirm-member'),

	# invite to group membership
	url(r'^social_group/(?P<social_group_id>[0-9]+)/user_invite/$', views.user_invite, name='user-invite'),
	# accept /decline invitation to a group
	url(r'^user_profile/(?P<user_profile_id>[0-9]+)/respond_member/$', views.respond_invitation, name='confirm-member'),

	#url for ajax search
	url(r'^social_group/(?P<social_group_id>[0-9]+)/video_search/$', views.video_search, name='video-search'),
	url(r'^social_group/(?P<social_group_id>[0-9]+)/user_search/$', views.user_search, name='user-search'),
	url(r'^user_profile/(?P<user_profile_id>[0-9]+)/group_search/$', views.group_search, name='group-search'),

	#make a comment on a tag
	url(r'^social_group/(?P<social_group_id>[0-9]+)/(?P<tag_id>[0-9]+)/tag/comment/$', views.comment, name='make-comment'),
	#make a comment on a video
	url(r'^(?P<vid_id>[0-9]+)/comment/$', views.comment, name='make-comment-video'),
	url(r'^(?P<vid_id>[0-9]+)/(?P<tag_time>[0-9]+)/(?P<social_group_id>[0-9]+)/start_group/comment/$', views.video, name='make-comment-group-time'),
	url(r'^(?P<vid_id>[0-9]+)/(?P<social_group_id>[0-9]+)/from_group/comment/$', views.comment, name='make-comment-video-group'),
	url(r'^(?P<vid_id>[0-9]+)/(?P<tag_time>[0-9]+)/start/comment/$', views.comment, name='make-comment-video-start'),
	url(r'^social_group/(?P<social_group_id>[0-9]+)/comment/$', views.comment, name='make-comment-group'),
	#/video/social_group/1/comment/"
	#from group at specific time??????

	#add a video to a group
	url(r'^social_group/(?P<social_group_id>[0-9]+)/link_video_group/$', views.link_video_group, name='link-video-group'),
	#update group settings
	url(r'^social_group/(?P<social_group_id>[0-9]+)/update_group/$', views.social_group, name='update-group-settings'),

	# video views
	url(r'^(?P<vid_id>[0-9]+)/$', views.video, name='video'),
	url(r'^(?P<vid_id>[0-9]+)/(?P<tag_time>[0-9]+)/start/$', views.video, name='video-time'),
	url(r'^(?P<vid_id>[0-9]+)/(?P<social_group_id>[0-9]+)/from_group/$', views.video, name='video-group'),
	url(r'^(?P<vid_id>[0-9]+)/(?P<social_group_id>[0-9]+)/(?P<poster_time_str>[0-9]+)/init/$', views.video, name='video-init'),
	url(r'^(?P<vid_id>[0-9]+)/(?P<tag_time>[0-9]+)/(?P<social_group_id>[0-9]+)/start_group/$', views.video, name='video-group-time'),
	#url(r'^(?P<vid_id>[0-9]+)/(?P<social_group_id>[0-9]+)/from_group/$', views.video_group_specific, name='video_group'),

	#url(r'^social_group/$', views.social_group_save, name='social_group_save'),
	url(r'^user_profile/$', views.user_profile_save_groups, name='user-profile-save-groups'),
	url(r'^social_group/(?P<social_group_id>[0-9]+)/$', views.social_group, name='social-group'),

	#url that goes to the slides page of a group
	url(r'^social_group/(?P<social_group_id>[0-9]+)/slides/$', views.social_group_slides, name='social-group-slides'),
	url(r'^social_group/(?P<social_group_id>[0-9]+)/slides/connect_slide/$', views.connect_user_slides, name='connect-user-slides'),
	#url(r'^slides/$', views.social_group_slides, name='upload-slide'),
	#tag page - within social group environment
	url(r'^social_group/(?P<social_group_id>[0-9]+)/(?P<tag_id>[0-9]+)/tag/$', views.tag_page, name='tag-page'),
	#url to add a tag to a collection

	#url to edit group settings page
	url(r'^social_group/(?P<social_group_id>[0-9]+)/settings/$', views.social_group_settings, name='social-group-settings'),
	#url for social group members page
	url(r'^social_group/(?P<social_group_id>[0-9]+)/members/$', views.social_group_members, name='social-group-members'),

	url(r'^social_group/(?P<social_group_id>[0-9]+)/(?P<tag_id>[0-9]+)/tag/collect_tag/$', views.collect_tag_page, name='collect-tag-page'),

	url(r'^social_group/(?P<social_group_id>[0-9]+)/(?P<tag_id>[0-9]+)/edit_tag/$', views.tag_page, name='edit-tag-page'),


	url(r'^user_profile/(?P<user_profile_id>[0-9]+)/$', views.user_profile, name='user-profile'),
	#slides page on userprofile
	url(r'^user_profile/(?P<user_profile_id>[0-9]+)/slides/$', views.user_profile_slides, name='user-profile-slides'),
	url(r'^user_profile/(?P<user_profile_id>[0-9]+)/groups/$', views.user_profile_groups, name='user-profile-groups'),
	url(r'^user_profile/(?P<user_profile_id>[0-9]+)/tags/$', views.user_profile_tags, name='user-profile-tags'),
	url(r'^user_profile/(?P<user_profile_id>[0-9]+)/videos/$', views.user_profile_videos, name='user-profile-videos'),
	#collections page on user profile
	url(r'^user_profile/(?P<user_profile_id>[0-9]+)/collections/$', views.user_profile_collections, name='user-profile-collections'),
	#individual collections page on user profile
	url(r'^user_profile/(?P<user_profile_id>[0-9]+)/collections/(?P<collection_id>[0-9]+)/$', views.user_profile_collection_solo, name='user-profile-collection-solo'),
	#collection creation from a specific tag page
	url(r'^user_profile/(?P<user_profile_id>[0-9]+)/collections/(?P<tag_id>[0-9]+)/$', views.user_profile_collections, name='collection-tag-page'),
	url(r'^connection/$', views.connection, name = 'public-connection'),
	url(r'^logout/$', views.log_out, name = 'log-out'),
	url(r'^search/', include('haystack.urls')),


    # ex: /polls/5/results/
#	url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
#	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

]