from django.urls import path, include
from . import views

app_name = 'admin'

urlpatterns = [
	path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
	path('register-user-send-email/', views.RegistrationURLView.as_view(), 
		name='register-user-send-email'),
	path('agent/registration-url/', views.AgentRegistrationURLView.as_view(), 
		name='agent-registration-url'),
]