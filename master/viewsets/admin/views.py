from master.viewsets.views import (AgentRegistrationURLView as BaseAgentRegistrationURLView, 
	RegistrationURLView as BaseRegistrationURLView)
from master.models import User, Manager
from django.urls import reverse_lazy
from .forms import RegistrationURLForm
from django.utils.translation import ugettext_lazy as _

class RegistrationURLView(BaseRegistrationURLView):
	template_name = 'master/admin/registration_form_email.html'
	success_url = reverse_lazy('admin:index')
	registration_path = 'master:users:manager:registration'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = _('Manager Registration Form')
		return context

class AgentRegistrationURLView(BaseAgentRegistrationURLView):
	template_name = 'master/admin/registration_form_email.html'
	success_url = reverse_lazy('admin:index')
	registration_path = 'master:users:agent:registration'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = _('Agent Registration Form')
		return context
