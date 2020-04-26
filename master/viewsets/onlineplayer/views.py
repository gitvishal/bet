from django.shortcuts import redirect, render
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from django.views.generic import TemplateView
from .forms import RegistrationForm
from django.urls import reverse_lazy
from .permissions import PermissionMixin
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationView(BaseRegistrationView):
	model = User
	form_class = RegistrationForm
	success_url = reverse_lazy('users:onlineplayer:auth_login')

class HomeView(PermissionMixin, TemplateView):
	template_name = 'online_player/home.html'