from django.shortcuts import redirect, render
from master.viewsets.views import (RegistrationView as BaseRegistrationView, 
	RegistrationURLView as BaseRegistrationURLView)
from django.views.generic import TemplateView
from .forms import UserCreationForm
from django.urls import reverse_lazy

class RegistrationView(BaseRegistrationView):
	form_class = UserCreationForm
	success_url = reverse_lazy('master:users:agent:home')

class HomeView(TemplateView):
	template_name = 'index.html'