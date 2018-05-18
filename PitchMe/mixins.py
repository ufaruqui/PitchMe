from django.utils.http import is_safe_url


class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class NextUrlMixin(object):
    default_next = "/"
    def get_next_url(self):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, request.get_host()):
                return redirect_path
        return self.default_next
		
		
class CheckUserTypeMixin(object):
	def get_context_data(self, queryset=None, **kwargs):
        # Call the base implementation first to get a context
		context = super(CheckUserTypeMixin, self).get_context_data(**kwargs)
		#Update Context with the can_edit
		#Your logic goes here (something like that)
		#if self.request.user == queryset.posted_by:
		if self.request.user == self.object.posted_by:
			context['is_job_poster']=True
		else:
			context['is_job_poster']=False
		
		context['is_applicant']=self.request.user.is_applicant
		return context