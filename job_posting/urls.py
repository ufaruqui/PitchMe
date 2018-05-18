from django.conf.urls import url
from . import views

from django.views.generic.base import TemplateView

app_name= 'job_posting'

urlpatterns = [
    # /job_posting/
	url(r'^$', views.IndexView.as_view(), name='index'),
	
	# /job_posting/all_jobs
	url(r'^all/$', views.AllJobsView.as_view(), name='all_jobs'),
	
	
	# /job_posting/register/
	#url(r'^register/$', views.IndexView.as_view(), name='register'),
		
	
	
	# /job_posting/job/add/
	url(r'job/add/$', views.JobCreate.as_view(), name='job-add'),
	
	# /job_posting/<applicant_id>/
	url(r'^(?P<pk>[0-9]+)/$', views.JobDetailView.as_view(), name='job-detail'),
	
	# /job_posting/job/2/delete/
	url(r'job/(?P<pk>[0-9]+)/delete/$', views.JobDelete.as_view(), name='job-delete'),
	
	
	
	# /job_posting/pitch/create/
	#url(r'apply/$', views.ApplicationCreate.as_view(), name='application-create'),
	url(r'application/create/(?P<pk>[0-9]+)$', views.PitchCreate.as_view(), name='pitch-create'),
	
	# /job_posting/applicant/2/
	#url(r'applicant/(?P<pk>[0-9]+)/$', views.ApplicationUpdate.as_view(), name='application-update'),

	# /job_posting/applicant/2/delete/
	url(r'applicant/(?P<pk>[0-9]+)/delete/$', views.PitchDelete.as_view(), name='pitch-delete'),
	
	
	# /job_posting/myVideos/2/
	url(r'myVideos/(?P<pk>[0-9]+)/$', views.VideosView.as_view(), name='myVideos'),
		
]
