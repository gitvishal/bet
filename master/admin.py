from django.contrib import admin, messages
from .models import *
from django.utils.translation import ugettext_lazy as _

@admin.register(Manager)
class AdminManager(admin.ModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation', 'user', 'parent',)
	list_per_page = 15

@admin.register(Supervisor)
class AdminSupervisor(admin.ModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation','user','parent',)
	list_per_page = 15

@admin.register(Employee)
class AdminEmployee(admin.ModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation','user','parent',)
	list_per_page = 15

@admin.register(OnlinePlayer)
class AdminOnlinePlayer(admin.ModelAdmin):
	list_display =('user', 'monitoring_user',)
	list_per_page = 15

@admin.register(Agent)
class AdminAgent(admin.ModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation','user','parent',)
	list_per_page = 15

@admin.register(AgentPlayer)
class AdminAgentPlayer(admin.ModelAdmin):
	search_fields = ('name', 'mobile', 'agent',)
	list_display = ('name', 'mobile', 'agent',)
	list_per_page = 15