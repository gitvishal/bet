from django.contrib import admin
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

admin.site.site_url = reverse_lazy('users:admin:dashboard')

class CustomModelAdmin(admin.ModelAdmin):
	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request):
		return False

@admin.register(SuperPotEvent)
class AdminSuperPotEvent(admin.ModelAdmin):
	search_fields = ('name', 'start_time', 'end_time')
	list_display =('name', 'start_time', 'end_time', 'days', 'created_on', 'created_by')
	exclude = ('created_by',)
	list_per_page = 15

	def has_delete_permission(self, request):
		return False

	def save_model(self, request, obj, form, change):
		obj.created_by = request.user
		super().save_model(request, obj, form, change)

@admin.register(SuperPot)
class AdminSuperPot(CustomModelAdmin):
	search_fields = ('status',)
	list_display =('event', 'started_on', 'ended_on', 'open_patti', 'close_patti', 'status',)
	list_per_page = 15

class AdminSuperPotBet(CustomModelAdmin):
	search_fields = ('transaction__transaction_id',)
	list_display =('player', 'transaction', 'created_on', 'pot', 'slip')
	list_per_page = 15

@admin.register(AgentPlayerSuperPotBet)
class AdminAgentPlayerSuperPotBet(AdminSuperPotBet):
	pass

@admin.register(OnlinePlayerSuperPotBet)
class AdminOnlinePlayerSuperPotBet(AdminSuperPotBet):
	pass