from master.viewsets.views import (RegistrationView as BaseRegistrationView, 
	RegistrationURLView as BaseRegistrationURLView)
from django.views.generic import TemplateView
from master.models import Employee, Supervisor
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

class RegistrationView(BaseRegistrationView):
	success_url = reverse_lazy('users:supervisor:home')

class HomeView(TemplateView):
	template_name = 'index.html'

class RegistrationURLView(BaseRegistrationURLView):
	template_name = 'master/supervisor/registration_form_email.html'
	success_url = reverse_lazy('users:supervisor:home')
	registration_path = 'users:manager:registration'
	title = _('Form to Send Email For Registration as Employee')

	def email_context(self, form):
		context = super().email_context(form)
		context['parent'] = {
			'module': Supervisor.__module__, 'model':Supervisor.__name__, 
			'params':{'user__email':self.request.user.email, 'user__user_type': self.request.user.user_type}
		}
		context['child'] = {
			'module': Employee.__module__, 'model':Employee.__name__,
			'params':{'designation': form.cleaned_data['designation']}
		}
		return context