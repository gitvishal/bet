from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from . import views

app_name = 'onlineplayer'

account_patterns = [
	path('login/',
		auth_views.LoginView.as_view(
			template_name='onlineplayer/registration/login.html'),
		name='auth_login'),
	path('registration/', views.RegistrationView.as_view(
			template_name='onlineplayer/registration/registration_form.html'), 
		name='registration'),
]

urlpatterns = [
	path('home', views.HomeView.as_view(), name='home'),
	path('accounts/', include(account_patterns)),
]
