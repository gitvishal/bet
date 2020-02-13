from django.urls import path, include
from . import views

app_name = 'agent'

urlpatterns = [
	path('home', views.HomeView.as_view(), name='home'),
	path('registration/agent/<str:token>/', views.AgentRegistrationView.as_view(), 
		name='agent-registration'),
	path('registration/subagent/<str:token>/', views.SubAgentRegistrationView.as_view(), 
		name='sub-agent-registration'),
]