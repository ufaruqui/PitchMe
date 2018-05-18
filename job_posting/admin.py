# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Job, Pitch, Company

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm #update view
    add_form = UserAdminCreationForm #create view

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin', 'applicant', 'recruiter')
    list_filter = ('admin', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'city', 'country', 'company')}),
        ('Account Type', {'fields': ('applicant', 'recruiter')}),
        ('Account Permissions', {'fields': ('admin', 'staff', 'active')}),
        ('Submissions', {'fields': ('vidResume1', 'vidResume2', 'highlight1','highlight2', 'traditionalResume')}),
		('Inputs from Wizard', {'fields': ('accomplishments','intro','body','conclusion')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Job)
admin.site.register(Pitch)
admin.site.register(Company)



# Remove Group Model from admin. We're not using it.
#admin.site.unregister(Group)