from master.viewsets.views import RegistrationView as BaseRegistrationView
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from master.models import User, Employee
from django.urls import reverse_lazy

class RegistrationView(BaseRegistrationView):
	one_to_one_model = Employee
	success_url = reverse_lazy('master:users:employee:home')

class HomeView(TemplateView):
	template_name = 'index.html'

