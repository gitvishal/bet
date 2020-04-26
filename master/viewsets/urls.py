from django.urls import path, include
from django.views.generic import TemplateView
from .views import AgentRegistrationURLView, HomeRemoteRedirectView

app_name = 'users'

urlpatterns = [
	path('', TemplateView.as_view(template_name='home.html'), name='home'),
	path('home-redirect/', HomeRemoteRedirectView.as_view(), name='home-redirect'),
	path('manager/', include('master.viewsets.manager.urls')),
	path('supervisor/', include('master.viewsets.supervisor.urls')),
	path('employee/', include('master.viewsets.employee.urls')),
	path('onlineplayer/', include('master.viewsets.onlineplayer.urls')),
	path('agent/', include('master.viewsets.agent.urls')),
	path('agent-registration/', AgentRegistrationURLView.as_view(), name='agent-register'),
	path('admin/', include('master.viewsets.admin.urls')),
	path('accounts/', include('registration.backends.default.urls')),
]