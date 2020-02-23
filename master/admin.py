from django.contrib import admin, messages
from .models import *
from django.utils.translation import ugettext_lazy as _

class CustomModelAdmin(admin.ModelAdmin):
	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request):
		return False

@admin.register(User)
class AdminUser(CustomModelAdmin):
	search_fields = ('user_type', 'username',)
	list_display =('user_type','username',)
	list_per_page = 15

	def get_queryset(self, *args, **kwargs):
		qs = super().get_queryset(*args, **kwargs).exclude(is_superuser=True)
		return qs

@admin.register(Manager)
class AdminManager(CustomModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation', 'user', 'parent',)
	list_per_page = 15

@admin.register(Supervisor)
class AdminSupervisor(CustomModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation','user','parent',)
	list_per_page = 15

@admin.register(Employee)
class AdminEmployee(CustomModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation','user','parent',)
	list_per_page = 15

@admin.register(OnlinePlayer)
class AdminOnlinePlayer(CustomModelAdmin):
	list_display =('user', 'monitoring_user',)
	list_per_page = 15

@admin.register(Agent)
class AdminAgent(CustomModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation','user','parent',)
	list_per_page = 15

@admin.register(AgentPlayer)
class AdminAgentPlayer(CustomModelAdmin):
	search_fields = ('name', 'mobile', 'agent',)
	list_display = ('name', 'mobile', 'agent',)
	list_per_page = 15