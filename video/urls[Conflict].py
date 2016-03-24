from django.conf.urls import url

from . import views
from . import my_views
from . import upload_video




urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^upload/$', upload_video.page, name='upload'),

	# ex: /polls/5/
	url(r'^(?P<vid_id>[0-9]+)/$', views.video, name='video'),


    # ex: /polls/5/results/
#	url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
#	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

]