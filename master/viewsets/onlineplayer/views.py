from django.shortcuts import redirect, render
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from django.views.generic import TemplateView
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationView(BaseRegistrationView):
	model = User
	form_class = RegistrationForm
	success_url = reverse_lazy('users:onlineplayer:home')

class HomeView(TemplateView):
	template_name = 'master/online_player/index.html'