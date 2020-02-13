from django.urls import path, include
from . import views

app_name = 'onlineplayer'

urlpatterns = [
	path('home', views.HomeView.as_view(), name='home'),
	path('registration/', views.RegistrationView.as_view(), name='registration'),
]