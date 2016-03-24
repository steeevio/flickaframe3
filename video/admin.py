from django.contrib import admin

# Register your models here.
from .models import Tag, Vid, SocialGroup, UserProfile, Membership, GroupSlide, Comment, Collection

class TagInline(admin.TabularInline):
	model = Tag
	extra = 2

class SocialGroupInline(admin.TabularInline):
	model = SocialGroup.group_video.through
	extra = 2	

class VideoInline(admin.TabularInline):
	model = Vid
	extra = 2

class MembershipInline(admin.TabularInline):
	model = Membership.group
	extra = 2
	

class VidAdmin(admin.ModelAdmin):
	fieldsets = [
		('Video File',{'fields':['video_file']}),
		('Youtube ID',{'fields':['youtube_id']}),
		('Privacy',{'fields':['private']}),
		(None, {'fields':['video_title']}),
		('Date information',{'fields':['pub_date']}),
		('Description',{'fields':['video_description']}),
		('File location',{'fields':['video_location']}),
		('Poster Image',{'fields':['poster']}),
		('User',{'fields':['user']}),
		('Base Group',{'fields':['base_group']}),
	]

	inlines = [TagInline, SocialGroupInline]
	list_display = ('video_title', 'pub_date')
	search_fields = ['video_title']
	#filter_horizontal = ('group_video')

class SocialGroupAdmin(admin.ModelAdmin):
	fieldsets = [
		('Group owner',{'fields':['group_owner']}),
		(None,{'fields':['group_title']}),
		('Group Description',{'fields':['group_description']}),
		('Group video',{'fields':['group_video']}),
		('Group Member',{'fields':['group_member']}),
		('Group Tags',{'fields':['tag_groups']}),
	]



	inlines = [VideoInline, SocialGroupInline, MembershipInline]
	list_display =('group_title')
	filter_horizontal = ('group_video')

class MembershipAdmin(admin.ModelAdmin):
	fieldsets = [
		('Group',{'fields':['group']}),
		('User',{'fields':['member']}),
		('Manager',{'fields':['manager']}),
		('Status',{'fields':['membership_status']}),
		
	]
	list_display = ('group', 'member', 'membership_status')



admin.site.register(Vid, VidAdmin)
admin.site.register(Tag)
admin.site.register(GroupSlide)
admin.site.register(SocialGroup)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Collection)
admin.site.register(Membership, MembershipAdmin)
