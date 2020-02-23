from django.contrib import admin, messages
from .models import *
from django.utils.translation import ugettext_lazy as _

class AdminManager(admin.ModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation', 'user', 'parent',)
	list_per_page = 15

admin.register(Manager, AdminManager)

class AdminSupervisor(admin.ModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation','user','parent',)
	list_per_page = 15

admin.register(Supervisor, AdminSupervisor)

class AdminEmployee(admin.ModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation','user','parent',)
	list_per_page = 15

admin.register(Employee, AdminEmployee)

class AdminOnlinePlayer(admin.ModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation','user','parent',)
	list_per_page = 15

admin.register(OnlinePlayer, AdminOnlinePlayer)

class AdminAgent(admin.ModelAdmin):
	search_fields = ('designation', 'user', 'parent',)
	list_display =('designation','user','parent',)
	list_per_page = 15

admin.register(Agent, AdminAgent)

class AdminAgentPlayer(admin.ModelAdmin):
	search_fields = ('name', 'mobile', 'agent',)
	list_display = ('name', 'mobile', 'agent',)
	list_per_page = 15

admin.register(AgentPlayer, AdminAgentPlayer)

# class AdminGame(admin.ModelAdmin):
# 	list_per_page = 15
# 	list_display =('name',)
# admin.site.register(Game, AdminGame)

# class AdminClubTeam(admin.ModelAdmin):
# 	list_per_page = 15
# 	list_display =('name',)
# admin.site.register(ClubTeam, AdminClubTeam)

# class AdminInterNationalPot(admin.ModelAdmin):
# 	list_per_page = 15
# 	list_display =('team_1', 'team_2', 'winning_team')
# admin.site.register(InterNationalPot, AdminInterNationalPot)

# class AdminClubPot(admin.ModelAdmin):
# 	list_per_page = 15
# 	list_display =('team_1', 'team_2', 'winning_team')
# admin.site.register(ClubPot, AdminClubPot)
