from django.contrib import admin, messages
from .models import *
from django.utils.translation import ugettext_lazy as _

class CustomModelAdmin(admin.ModelAdmin):
	def has_add_permission(self, request):
		return False
		
	def has_delete_permission(self, request):
		return False
		
@admin.register(Transaction)
class AdminTransaction(CustomModelAdmin):
	search_fields = ('transaction_id', 'amount', 'confirmed','status')
	list_display = ('transaction_id', 'amount', 'confirmed','status')
	list_per_page = 15

@admin.register(AgentBalanceAccount)
class AdminAgentBalanceAccount(CustomModelAdmin):
	search_fields = ('transaction_type', 'transaction', 'agent',)
	list_display = ('transaction_type', 'transaction', 'agent',)
	list_per_page = 15

@admin.register(OnlinePlayerBalanceAccount)
class AdminOnlinePlayerBalanceAccount(CustomModelAdmin):
	search_fields = ('transaction_type', 'transaction', 'player',)
	list_display = ('transaction_type', 'transaction', 'player',)
	list_per_page = 15