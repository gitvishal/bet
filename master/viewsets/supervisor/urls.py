from django.urls import path, include
from . import views

app_name = 'supervisor'

urlpatterns = [
	path('home', views.HomeView.as_view(), name='home'),
	path('registration/<str:token>/', views.RegistrationView.as_view(), name='registration'),
	path('register-user-send-email/', views.RegistrationURLView.as_view(), name='register-user-send-email'),
]