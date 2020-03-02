from django.urls import path, include

from . import views

app_name = 'master'

urlpatterns = [
	path('home/', views.HomeRemoteRedirectView.as_view(), name='home'),
	path('user/', include('master.viewsets.urls')),
	path('accounts/', include('registration.backends.simple.urls')),
]

