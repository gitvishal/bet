from django.urls import path, include
from . import views

app_name = 'agent'

urlpatterns = [
	path('home', views.HomeView.as_view(), name='home'),
	path('registration/agent/<str:token>/', views.RegistrationView.as_view(), 
		name='agent-registration'),
]