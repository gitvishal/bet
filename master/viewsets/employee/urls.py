from django.urls import path, include
from . import views

app_name = 'employee'

urlpatterns = [
	path('home', views.HomeView.as_view(), name='home'),
	path('registration/<str:token>/', views.RegistrationView.as_view(), name='registration'),
]