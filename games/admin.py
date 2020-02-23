from django.contrib import admin, messages
from .models import *
from django.utils.translation import ugettext_lazy as _

@admin.register(Game)
class AdminGame(admin.ModelAdmin):
	search_fields = ('name',)
	list_display = ('name', 'photo',)
	list_per_page = 15

@admin.register(ClubTeam)
class AdminClubTeam(admin.ModelAdmin):
	search_fields = ('name',)
	list_display = ('name', 'photo',)
	list_per_page = 15

@admin.register(InterNationalPot)
class AdminInterNationalPot(admin.ModelAdmin):
	list_display = ('team_1', 'team_2','winning_team')
	list_per_page = 15

@admin.register(ClubPot)
class AdminClubPot(admin.ModelAdmin):
	list_display = ('team_1', 'team_2','winning_team')
	list_per_page = 15

@admin.register(SuperPotEvent)
class AdminSuperPotEvent(admin.ModelAdmin):
	list_display = ('name', 'created_on','created_by')
	list_per_page = 15

@admin.register(SuperPot)
class AdminSuperPot(admin.ModelAdmin):
	list_display = ('ended_on', 'open_patti', 'close_patti', 'status',)
	list_per_page = 15

@admin.register(AgentPlayerSuperPotBet)
class AdminAgentPlayerSuperPotBet(admin.ModelAdmin):
	list_display = ('created_on', 'player', 'transaction',)
	list_per_page = 15

@admin.register(OnlinePlayerSuperPotBet)
class AdminOnlinePlayerSuperPotBet(admin.ModelAdmin):
	list_display = ('created_on', 'player', 'transaction',)
	list_per_page = 15