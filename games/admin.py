from django.contrib import admin, messages
from .models import *
from django.utils.translation import ugettext_lazy as _

class AdminGame(admin.ModelAdmin):
	search_fields = ('name',)
	list_display = ('name', 'photo',)
	list_per_page = 15

admin.register(Game, AdminGame)

class AdminClubTeam(admin.ModelAdmin):
	search_fields = ('name',)
	list_display = ('name', 'photo',)
	list_per_page = 15

admin.register(ClubTeam, AdminClubTeam)

class AdminInterNationalPot(admin.ModelAdmin):
	list_display = ('team_1', 'team_2','winning_team')
	list_per_page = 15

admin.register(InterNationalPot, AdminInterNationalPot)

class AdminClubPot(admin.ModelAdmin):
	list_display = ('team_1', 'team_2','winning_team')
	list_per_page = 15

admin.register(ClubPot, AdminClubPot)

class AdminSuperPotEvent(admin.ModelAdmin):
	list_display = ('name', 'created_on','created_by')
	list_per_page = 15

admin.register(SuperPotEvent, AdminSuperPotEvent)

class AdminSuperPot(admin.ModelAdmin):
	list_display = ('created_on', 'player', 'ended_on', 'open_patti', 'close_patti', 'status',)
	list_per_page = 15

admin.register(SuperPot, AdminSuperPot)

class AdminAgentPlayerSuperPotBet(admin.ModelAdmin):
	list_display = ('created_on', 'player', 'transaction',)
	list_per_page = 15

admin.register(AgentPlayerSuperPotBet, AdminAgentPlayerSuperPotBet)

class AdminOnlinePlayerSuperPotBet(admin.ModelAdmin):
	list_display = ('created_on', 'player', 'transaction',)
	list_per_page = 15

admin.register(OnlinePlayerSuperPotBet, AdminOnlinePlayerSuperPotBet)