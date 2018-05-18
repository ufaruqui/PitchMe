"""PitchMe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from job_posting import views

from django.urls import reverse_lazy
from django.contrib.auth.views import(LogoutView)

urlpatterns = [
	
	
	url(r'^admin/', admin.site.urls),
	
	# /login/
	url(r'^login/$', views.LoginView.as_view(), name='login'),
			
	# /logout/
	url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
	
	# /profile/
	url(r'^profile/(?P<pk>[0-9]+)$', views.UserUpdate.as_view(), name='profile'),
	
	url(r'^job_posting/', include('job_posting.urls')),
	
]

if settings.DEBUG:
	urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	