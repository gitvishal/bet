from django.urls import path, include
from . import views

app_name = 'admin'

urlpatterns = [
	path('manager/registration-url/', views.RegistrationURLView.as_view(), 
		name='manager-registration-url'),
	path('agent/registration-url/', views.AgentRegistrationURLView.as_view(), 
		name='agent-registration-url'),
]