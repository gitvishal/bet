from master.viewsets.views import (RegistrationView as BaseRegistrationView, 
	RegistrationURLView as BaseRegistrationURLView)
from django.views.generic import TemplateView
from master.models import Manager, Supervisor
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

class RegistrationView(BaseRegistrationView):
	success_url = reverse_lazy('users:manager:home')

class RegistrationURLView(BaseRegistrationURLView):
	success_url = reverse_lazy('users:manager:home')
	registration_path = 'users:manager:registration'
	title = _('Form to Send Email For Registration as Supervisor')

	def email_context(self, form):
		context = super().email_context(form)
		context['parent'] = {
			'module': Manager.__module__, 'model':Manager.__name__, 
			'params':{'user__email':self.request.user.email, 'user__user_type': self.request.user.user_type}
		}
		context['child'] = {
			'module': Supervisor.__module__, 'model':Supervisor.__name__,
			'params':{'designation': form.cleaned_data['designation']}
		}
		return context

class HomeView(TemplateView):
	template_name = 'index.html'

