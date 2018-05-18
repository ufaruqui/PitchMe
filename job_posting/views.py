from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from django.views import generic
from django.views.generic import View
from django.conf import settings
from .models import User,Job, Pitch
from django.views.generic import TemplateView,DetailView, FormView, RedirectView
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import LoginForm, RegisterForm

from django.contrib.auth.mixins import LoginRequiredMixin
from PitchMe.mixins import NextUrlMixin, RequestFormAttachMixin, CheckUserTypeMixin

import datetime

class IndexView(LoginRequiredMixin,generic.ListView):	
	
	context_object_name='jobs'
	
	def get_queryset(self):		
		if self.request.user.is_recruiter:
			#retrieve all jobs posted by logged-in user
			return Job.objects.all().filter(posted_by=self.request.user)			
		else:
			#retrieve all applications by logged-in user
			return Pitch.objects.all().filter(applicant=self.request.user)
	
	def get_template_names(self):
		if self.request.user.is_recruiter:
			return ['job_posting/index.html'] 
		else:
			return ['job_posting/index_applicant.html']
	
	
class AllJobsView(LoginRequiredMixin,generic.ListView):	
	
	template_name= 'job_posting/all.html'
	context_object_name='jobs'
	
	#retrieve all jobs in the database
	def get_queryset(self):
		return Job.objects.all()
	
	
	
	
class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = 'job_posting:index'
    template_name = 'job_posting/login.html'
    default_next = 'job_posting:index'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)
		
class UserUpdate(LoginRequiredMixin,UpdateView):
	model=User
		
	def dispatch(self, request, *args, **kwargs):
		# Display fields based on type of user
		if self.request.user.is_recruiter:
			self.fields = fields=['first_name', 'last_name', 'city', 'country',	'company']
		else:
			self.fields = fields=['first_name', 'last_name', 'city', 'country',	'company', 'highlight1', 'highlight2', 'traditionalResume']
		return super(UserUpdate, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, form):
		return super(UserUpdate, self).form_valid(form)




		
class VideosView(LoginRequiredMixin, UpdateView):
	model=User
	fields=['vidResume1',
	'vidResume2',
	'accomplishments',
	'intro',
	'body',
	'conclusion']
	template_name='job_posting/myVideos.html'
	
	
	def get_success_url(self):
		return reverse_lazy('job_posting:myVideos', kwargs={'pk': self.request.user.id})
		
		
	def form_valid(self, form):
		return super(VideosView, self).form_valid(form)
	

		
#class SignUpView(TemplateView):
#    template_name = 'registration/signup.html'



class JobCreate(LoginRequiredMixin,CreateView):
	model=Job
	fields=['job_title', 'company_name','job_description']	

	def form_valid(self, form):
		form.instance.posted_by = self.request.user
		return super(JobCreate, self).form_valid(form)

class JobDetailView(LoginRequiredMixin, CheckUserTypeMixin, generic.DetailView):
	model=Job
	template_name= 'job_posting/job_details.html'

#class JobUpdate(UpdateView):
#	model=Job
#	fields=['job_title', 'company_name','job_description']
	
class JobDelete(LoginRequiredMixin,DeleteView):
	model=Job
	success_url=reverse_lazy('job_posting:index')
		
	
	
class PitchCreate(LoginRequiredMixin,CreateView):
	model=Pitch	
	fields=['video']
	
	def form_valid(self, form):
		form.instance.applicant = self.request.user
		form.instance.job = Job.objects.get(pk=self.kwargs.get('pk'))
		form.instance.pitch_submitted=datetime.datetime.now()
		return super(PitchCreate, self).form_valid(form)
		
class PitchDelete(LoginRequiredMixin,DeleteView):
	model=Pitch
	success_url=reverse_lazy('job_posting:index')


	
