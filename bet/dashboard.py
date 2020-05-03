"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
	GRAPPELLI_INDEX_DASHBOARD = 'bet.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.urls import reverse, reverse_lazy

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):

	def init_with_context(self, context):
		site_name = get_admin_site_name(context)

		self.children.append(modules.Group(
			_('All Betting Applications'),
			column=1,
			collapsible=True,
			children = [
				modules.ModelList(
					_('Administration'),
					column=1,
					models=('django.contrib.*',),
				),
				modules.ModelList(
					_('Hierarchy Users'),
					column=1,
					models=(
						'master.models.users.Manager', 
						'master.models.users.Supervisor',
						'master.models.users.Employee',
						'master.models.users.Agent',
					),
				),
				modules.ModelList(
					_('SuperPot'),
					column=1,
					models=(
						'games.models.superpot.SuperPotEvent', 
						'games.models.superpot.SuperPot',
						'games.models.superpot.SuperPotSlip',
						'games.models.superpot.AgentPlayerSuperPotBet',
						'games.models.superpot.OnlinePlayerSuperPotBet',
					),
				),
				modules.ModelList(
					_('Players'),
					column=1,
					models=(
						'master.models.users.OnlinePlayer', 
						'master.models.users.AgentPlayer',
					),
				),
				modules.ModelList(
					_('Transactions'),
					column=1,
					models=(
						'master.models.payments.AgentBalanceAccount', 
						'master.models.payments.OnlinePlayerBalanceAccount',
					),
				),

			]
		))

		self.children.append(modules.LinkList(
			_('Extra Admin Options'),
			column=2,
			children=(
				(
					'Generate Manager Registration Link', 
					reverse_lazy('users:admin:register-user-send-email')
				),
				(
					'Generate Agent Registration Link', 
					reverse_lazy('users:admin:agent-registration-url')
				),
			)
		))

		self.children.append(modules.Group(
			_('Latest Cricket Feeds'),
			column=2,
			collapsible=True,
			children = [
				modules.Feed(
					_('Latest Cricket News'),
					column=2,
					feed_url='http://static.cricinfo.com/rss/livescores.xml',
					limit=5
				),
				modules.Feed(
					_('Latest ESPN Cricket News'),
					column=2,
					feed_url='https://www.espn.co.uk/espn/rss/cricket/news',
					limit=5
				)
			]
		))

		self.children.append(modules.RecentActions(
			_('Recent Actions'),
			limit=5,
			collapsible=False,
			column=3,
		))
