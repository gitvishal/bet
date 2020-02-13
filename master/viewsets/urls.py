from django.urls import path, include

app_name = 'users'

urlpatterns = [
	path('manager/', include('master.viewsets.manager.urls')),
	path('supervisor/', include('master.viewsets.supervisor.urls')),
	path('employee/', include('master.viewsets.employee.urls')),
	path('onlineplayer/', include('master.viewsets.onlineplayer.urls')),
	path('agent/', include('master.viewsets.agent.urls')),
	path('admin/', include('master.viewsets.admin.urls')),
]