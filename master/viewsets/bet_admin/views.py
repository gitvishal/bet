from master.views import (AgentRegistrationURLView as BaseAgentRegistrationURLView, 
	RegistrationURLView as BaseRegistrationURLView, ManagementHomeView as BaseManagementHomeView)
from .permissions import UserPermissionMixin
from django.views.generic import TemplateView, View
from master.models import User, Manager
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

class DashboardView(UserPermissionMixin, BaseManagementHomeView):
	template_name = 'bet_admin/dashboard.html'

class RegistrationURLView(BaseRegistrationURLView):
	template_name = 'bet_admin/registration_form_email.html'
	success_url = reverse_lazy('admin:index')
	registration_path = 'users:manager:registration'
	title = _('Form to Send Email For Registration as Manager')

	def email_context(self, form):
		context = super().email_context(form)
		context['parent'] = {
			'module': User.__module__, 'model':User.__name__, 
			'params':{'email':self.request.user.email, 
				'user_type': self.request.user.user_type,
				'is_superuser':True
			}
		}
		context['child'] = {
			'module': Manager.__module__, 'model':Manager.__name__,
			'params':{'designation': form.cleaned_data['designation']}
		}
		return context

class AgentRegistrationURLView(BaseAgentRegistrationURLView):
	template_name = 'bet_admin/registration_form_email.html'
	success_url = reverse_lazy('admin:index')