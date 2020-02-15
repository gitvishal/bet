from master.viewsets.views import (RegistrationView as BaseRegistrationView, 
	RegistrationURLView as BaseRegistrationURLView)
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from master.models import Supervisor, Employee
from django.urls import reverse_lazy

class RegistrationView(BaseRegistrationView):
	one_to_one_model = Employee
	parent_model = Supervisor
	success_url = reverse_lazy('master:users:employee:home')

class HomeView(TemplateView):
	template_name = 'index.html'

