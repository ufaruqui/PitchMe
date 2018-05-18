# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from datetime import datetime
import os

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')		
        if not password:
			raise ValueError('Users must have a password')
			
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
	
	
  
class User(AbstractBaseUser):
	email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
	)   
	
	###Personal Info###
	first_name= models.CharField(max_length=30)
	last_name= models.CharField(max_length=30)
	city= models.CharField(max_length=30)
	country= models.CharField(max_length=30)
	company= models.CharField(max_length=30, blank=True)
	#profile_picture= models.FileField()
	
	###Account Type###
	applicant= models.BooleanField(default=False)
	recruiter= models.BooleanField(default=False)
	
	###Account Permissions###
	active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False) # a admin user; non super-user
	admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.

	###Submissions###
	vidResume1= models.FileField(blank=True)
	vidResume2= models.FileField(blank=True)
	
	#Limit highlights to 1000 characters
	highlight1=models.CharField(max_length=1000, blank=True)
	highlight2=models.CharField(max_length=1000, blank=True)
	
	traditionalResume= models.FileField(blank=True)
	
	#Inputs from Wizard
	accomplishments=models.TextField(max_length=1000, blank=True)
	intro=models.TextField(max_length=1000, blank=True)
	body=models.TextField(max_length=1000, blank=True)
	conclusion=models.TextField(max_length=1000, blank=True)
	
		
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [] # Email & Password are required by default.

	objects = UserManager()
	
	def get_full_name(self):		
		return self.first_name + " " + self.last_name

	def get_short_name(self):
		return self.first_name
	
	def get_absolute_url(self):
		return reverse('profile', kwargs={'pk':self.pk})
	
	def __str__(self):
		return self.first_name + " " + self.last_name

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	def vidResume1ToStr(self):
		return os.path.basename(self.vidResume1.name)
	
	def vidResume2ToStr(self):
		return os.path.basename(self.vidResume2.name)
	
	def traditionalResumeToStr(self):
		return os.path.basename(self.traditionalResume.name)
	
	@property
	def is_active(self):
		"Is the user active?"
		return self.active
	
	@property
	def is_staff(self):
		"Is the user a member of staff?"
		return self.staff
	
	@property
	def is_admin(self):
		"Is the user an admin member?"
		return self.admin
	
	@property
	def is_applicant(self):
		"Is the user an applicant?"
		return self.applicant
	
	@property
	def is_recruiter(self):
		"Is the user a recruiter?"
		return self.recruiter

		
class Job(models.Model):
	job_title=models.CharField(max_length=30)
	company_name=models.CharField(max_length=30)
	job_description=models.CharField(max_length=1000)
	posted_by= models.ForeignKey(User,on_delete=models.CASCADE)	
	job_pitches= models.ManyToManyField('Pitch', related_name='+', blank=True)
		
	def get_absolute_url(self):
		return reverse('job_posting:job-detail', kwargs={'pk':self.pk})
	
	def __str__(self):
		return self.job_title + ' - ' + self.company_name		

		
				
class Pitch(models.Model):
	applicant= models.ForeignKey(User,on_delete=models.CASCADE)
	job = models.ForeignKey(Job,on_delete=models.CASCADE)
	pitch_submitted = models.DateTimeField(default=datetime.now(), blank=True)
	
	VIDEO_RESUME_CHOICES = (
	("1", "1"),
	("2", "2"),)
	
	video = models.CharField(max_length=9, choices=VIDEO_RESUME_CHOICES, default='1')
		
	def get_absolute_url(self):
	#	return reverse('job_posting:application-detail', kwargs={'pk':self.pk})
		return reverse('job_posting:index')
	
	def __str__(self):
		return self.applicant.__str__() + ' - ' + self.job.__str__()

		


	

class Company(models.Model):
	company_name= models.CharField(max_length=30)
	
	def __str__(self):
		return self.job_title + ' - ' + self.company_name	