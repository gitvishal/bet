from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField
from master.models.master import HistoricalModels
from master.models.users import AgentPlayer, OnlinePlayer, User
from master.models.payments import AgentBalanceAccount, OnlinePlayerBalanceAccount
from django.utils.translation import ugettext_lazy as _


class SuperPotEvent(HistoricalModels):
	name = models.CharField(max_length=45, help_text=_('Display Perpose'))
	created_on = models.DateTimeField(auto_now_add=True)
	created_by =models.ForeignKey(User, related_name='%(class)s_created_by', on_delete=models.PROTECT)
	#time is not yet decided

	def __str__(self):
		return f'{self.name} : {self.created_on}'

class SuperPot(HistoricalModels):
	IN_PROCESS = 'in-process'
	OPEN_DECLAIRED = 'open-declaired'
	CLOSE_DECLAIRED = 'close-declaired'

	BET_STATUS_CHOICES = (
		(IN_PROCESS, _('In Process')),
		(OPEN_DECLAIRED, _('Open')),
		(CLOSE_DECLAIRED, _('Close')), 
		
	)

	event = models.ForeignKey(SuperPotEvent, related_name='%(class)s_event', on_delete=models.PROTECT)
	started_on = models.DateTimeField(auto_now_add=True,)
	ended_on = models.DateTimeField(blank=True, null=True)
	open_patti = models.CharField(max_length=3, blank=True, null=True)
	close_patti = models.CharField(max_length=3, blank=True, null=True)
	status = models.CharField(max_length=25, choices=BET_STATUS_CHOICES, default=IN_PROCESS)

	def __str__(self):
		return f'{self.open_patti} x {self.close_patti}'

class SuperPotSlip(HistoricalModels):
	created_on = models.DateTimeField(auto_now_add=True,)
	slug = AutoSlugField(populate_from='get_random_string', unique=True)

	def __str__(self):
		return str(self.slug)

	def get_random_string(self):
		return get_random_string(length=10)

class SuperPotBet(HistoricalModels):
	PATTI_FORMAT = (
		(r'^\dx$', 'open', 9),
		(r'^x\d$', 'close', 9),
		(r'^\d{2}$', 'number', 90),
		(r'^\d{3}x$', 'open patti', 120),
		(r'^x\d{3}$', 'close patti', 120),
		(r'^\dx\d{3}$', 'half open sangam', 1080),
		(r'^\d{3}x\d$', 'half close sangam', 1080),
		(r'^\d{3}x\d{3}$', 'full sangam', 14400),

	)
	created_on = models.DateTimeField(auto_now_add=True,)
	pot = models.ForeignKey(SuperPot, related_name='%(class)s_pot', on_delete=models.PROTECT)
	slip = models.ForeignKey(SuperPotSlip, related_name='%(class)s_slip', on_delete=models.PROTECT)

	def __str__(self):
		return str(self.created_on)

	class Meta:
		abstract = True

class AgentPlayerSuperPotBet(SuperPotBet):
	player = models.ForeignKey(AgentPlayer, related_name='%(class)s_player', on_delete=models.PROTECT)
	transaction = models.OneToOneField(AgentBalanceAccount, on_delete=models.PROTECT, related_name='%(class)s_transaction',)

	def __str__(self):
		return str(self.transaction)

class OnlinePlayerSuperPotBet(SuperPotBet):
	player = models.ForeignKey(OnlinePlayer, related_name='%(class)s_player', on_delete=models.PROTECT)
	transaction = models.OneToOneField(OnlinePlayerBalanceAccount, on_delete=models.PROTECT, related_name='%(class)s_transaction',)

	def __str__(self):
		return str(self.transaction)