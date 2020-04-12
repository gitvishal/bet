from master.viewsets.views import (RegistrationView as BaseRegistrationView, 
	RegistrationURLView as BaseRegistrationURLView)
from django.views.generic import TemplateView
from django.urls import reverse_lazy

class RegistrationView(BaseRegistrationView):
	success_url = reverse_lazy('users:employee:home')

class HomeView(TemplateView):
	template_name = 'index.html'

