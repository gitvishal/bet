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
	"""
	Custom index dashboard for www.
	"""

	def init_with_context(self, context):
		site_name = get_admin_site_name(context)

		# append a group for "Administration" & "Applications"
		self.children.append(modules.Group(
			_('All Betting Applications'),
			column=1,
			collapsible=True,
			children = [
				modules.AppList(
					_('Applications'),
					column=2,
					css_classes=('collapse closed',),
					exclude=('django.contrib.*',),
				),
				modules.ModelList(
					_('Administration'),
					column=1,
					models=('django.contrib.*',),
				),
			]
		))

		# append another link list module for "support".
		self.children.append(modules.LinkList(
			_('Extra Admin Options'),
			column=2,
			children=(
				(
					'Generate Manager Registration Link', 
					reverse_lazy('master:users:admin:manager-registration-url')
				),
				(
					'Generate Agent Registration Link', 
					reverse_lazy('master:users:admin:agent-registration-url')
				),
			)
		))

		# append a feed module

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

		# append a recent actions module
		self.children.append(modules.RecentActions(
			_('Recent Actions'),
			limit=5,
			collapsible=False,
			column=3,
		))
