from django.db import models
from jsonfield import JSONField
from simple_history.models import HistoricalRecords
from .master import HistoricalModels
from .users import OnlinePlayer, Agent, User
from django_cryptography.fields import encrypt
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from django.shortcuts import reverse
import uuid

class Transaction(HistoricalModels):

	INPROCESS = 'inprocess'
	SUCCESS = 'success'
	FAILED = 'failed'

	STATUS_CHOICES = (
		(INPROCESS, _('in process')), 
		(SUCCESS, _('success')), 
		(FAILED, _('failed'))
	)

	transaction_id = models.CharField(max_length=45, unique=True,)
	amount = encrypt(models.DecimalField(max_digits=10, decimal_places=2))
	reason = encrypt(RichTextField())
	meta_data = encrypt(JSONField(blank=True, null=True))
	confirmed = models.BooleanField(default=False,)
	status = models.CharField(max_length=45, choices=STATUS_CHOICES,)
	
	def __str__(self):
		return str(self.transaction_id)

class BalanceAccount(HistoricalModels):

	CREDIT = 'credit'
	DEBIT = 'debit'

	TRANSACTION_TYPE_CHOICES = ((CREDIT, _('credit')), (DEBIT, _('debit')),)
	transaction = models.OneToOneField(Transaction, related_name='%(class)s_trans', on_delete=models.PROTECT)
	transaction_type = models.CharField(max_length=45, choices=TRANSACTION_TYPE_CHOICES,)
	created_on = models.DateTimeField(auto_now_add=True,)

	class Meta:
		abstract = True

class AgentBalanceAccount(BalanceAccount):
	agent = models.ForeignKey(Agent, related_name='%(class)s_agent', on_delete=models.PROTECT)

	def __str__(self):
		return str(self.transaction.transaction_id)

	class Meta:
		unique_together = ('agent', 'transaction',)

class OnlinePlayerBalanceAccount(BalanceAccount):
	player = models.ForeignKey(OnlinePlayer, related_name='%(class)s_online_player', on_delete=models.PROTECT)

	def __str__(self):
		return str(self.transaction.transaction_id)

	class Meta:
		unique_together = ('player', 'transaction',)

	# def get_absolute_url(self):
	# 	return reverse('djangobin:trending_snippets', args=[self.slug])

