from master.viewsets.views import (RegistrationView as BaseRegistrationView, 
	RegistrationURLView as BaseRegistrationURLView)
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from master.models import Manager, Supervisor
from django.urls import reverse_lazy
from .forms import RegistrationURLForm

class RegistrationView(BaseRegistrationView):
	one_to_one_model = Supervisor
	parent_model = Manager
	success_url = reverse_lazy('master:users:supervisor:home')

class HomeView(TemplateView):
	template_name = 'index.html'

class RegistrationURLView(BaseRegistrationURLView):
	form_class = RegistrationURLForm
	template_name = 'master/supervisor/registration_form_email.html'
	success_url = reverse_lazy('master:users:supervisor:home')