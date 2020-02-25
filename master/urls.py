from django.urls import path, include

from . import views

app_name = 'master'

urlpatterns = [
	path('', views.HomeView.as_view(), name='home'),
	path('user/', include('master.viewsets.urls')),
	path('accounts/', include('registration.backends.simple.urls')),
]

