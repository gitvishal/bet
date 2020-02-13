from django.contrib import admin, messages
from .models import *
from django.utils.translation import ugettext_lazy as _

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
