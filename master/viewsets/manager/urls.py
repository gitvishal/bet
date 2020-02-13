from django.urls import path, include
from . import views

app_name = 'manager'

urlpatterns = [
	path('home', views.HomeView.as_view(), name='home'),
	path('registration/<str:token>/', views.RegistrationView.as_view(), name='registration'),
]