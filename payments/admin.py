from django.contrib import admin, messages
from .models import *
from django.utils.translation import ugettext_lazy as _

class AdminTransaction(admin.ModelAdmin):
	search_fields = ('transaction_id', 'amount', 'confirmed','status')
	list_display = ('transaction_id', 'amount', 'confirmed','status')
	list_per_page = 15

admin.register(Transaction, AdminTransaction)

class AdminAgentBalanceAccount(admin.ModelAdmin):
	search_fields = ('transaction_type', 'transaction', 'agent',)
	list_display = ('transaction_type', 'transaction', 'agent',)
	list_per_page = 15

admin.register(AgentBalanceAccount, AdminAgentBalanceAccount)

class AdminOnlinePlayerBalanceAccount(admin.ModelAdmin):
	search_fields = ('transaction_type', 'transaction', 'player',)
	list_display = ('transaction_type', 'transaction', 'player',)
	list_per_page = 15

admin.register(OnlinePlayerBalanceAccount, AdminOnlinePlayerBalanceAccount)