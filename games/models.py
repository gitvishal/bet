from django.db import models
from simple_history.models import HistoricalRecords
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _
from master.models import IPAddressHistoricalModel, AgentPlayer, OnlinePlayer, User
from payments.models import AgentBalanceAccount, OnlinePlayerBalanceAccount
from django_countries.fields import CountryField
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from django.utils  import timezone

def file_path(instance, fname):
	d = timezone.now()
	return 'doc/{0}/{1}/{2}/{3}/{4}'.format(d.year, d.strftime('%B'), d.day, uuid.uuid4(), fname)

class Game(models.Model): ## game category
	name = models.CharField(max_length=45, unique=True)
	photo = ThumbnailerImageField(upload_to=file_path, max_length=500)
	history = HistoricalRecords(bases=[IPAddressHistoricalModel,])
 
	def __str__(self):
		return self.name

class ClubTeam(models.Model):
	"""state team or club team"""
	name = models.CharField(max_length=45, unique=True, help_text='club name or state name')
	photo = ThumbnailerImageField(upload_to=file_path, max_length=500, help_text='club flag or state flag')
	history = HistoricalRecords(bases=[IPAddressHistoricalModel,])

	def __str__(self):
		return self.name

class Pot(models.Model):
	game = models.ForeignKey(Game, related_name='%(class)s_game', on_delete=models.PROTECT)
	photo = ThumbnailerImageField(upload_to=file_path, max_length=500, blank=True, null=True)
	commission = models.PositiveIntegerField(default=10, help_text='In percentage')
	starts_on = models.DateTimeField()
	description = RichTextField(blank=True, null=True)
	created_on = models.DateTimeField(auto_now_add=True,)
	updated_on = models.DateTimeField(auto_now=True,)
	created_by = models.ForeignKey(User, related_name='%(class)s_by', on_delete=models.PROTECT)
	is_active = models.BooleanField(default=False,)
	history = HistoricalRecords(bases=[IPAddressHistoricalModel,], inherit=True)

	class Meta:
		abstract = True

	def __str__(self):
		return f'{self.game}:{self.starts_on}'

class InterNationalPot(Pot):
	team_1 = CountryField(blank_label=_('(select country)'))
	team_2 = CountryField(blank_label=_('(select country)'))
	winning_team = CountryField(blank_label=_('(select country)'), blank=True, null=True)

	def __str__(self):
		return f'{self.game}:{self.starts_on}'


class ClubPot(Pot):
	team_1 = models.ForeignKey(ClubTeam, related_name='%(class)s_team_1', on_delete=models.PROTECT)
	team_2 = models.ForeignKey(ClubTeam, related_name='%(class)s_team_2', on_delete=models.PROTECT)
	winning_team = models.ForeignKey(ClubTeam, related_name='%(class)s_win_team', 
		on_delete=models.PROTECT, blank=True, null=True)

	def __str__(self):
		return f'{self.game}:{self.starts_on}'

class SuperPotEvent(models.Model):
	name = models.CharField(max_length=45, help_text=_('Display Perpose'))
	created_on = models.DateTimeField(auto_now_add=True)
	created_by =models.ForeignKey(User, related_name='%(class)s_created_by', on_delete=models.PROTECT)
	#time is not yet decided
	history = HistoricalRecords(bases=[IPAddressHistoricalModel,])

	def __str__(self):
		return f'{self.name} : {self.created_on}'

class SuperPot(models.Model):
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
	history = HistoricalRecords(bases=[IPAddressHistoricalModel,],)

	def __str__(self):
		return f'{self.open_patti} x {self.close_patti}'

class SuperPotSlip(models.Model):
	created_on = models.DateTimeField(auto_now_add=True,)
	slug = AutoSlugField(populate_from='get_random_string', unique=True)
	history = HistoricalRecords(bases=[IPAddressHistoricalModel,], inherit=True)

	def __str__(self):
		return str(self.slug)

	def get_random_string(self):
		return get_random_string(length=10)

class SuperPotBet(models.Model):
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
	history = HistoricalRecords(bases=[IPAddressHistoricalModel,], inherit=True)

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
### 
# patti generating code

# from django.utils.crypto import get_random_string
# patti = sorted(get_random_string(length=3, allowed_chars='o123456789'))).replace('o', '0')
#
# number = sum(map(int, patti))%10


# class Bet(models.Model):
# 	IN_PROCESS = 'in-process'
# 	CONFIRMED = 'confirmed'
# 	NO_MATCH = 'no-match'
# 	PARTIAL_MATCH = 'partial-match'

# 	BET_STATUS_CHOICES = (
# 		(IN_PROCESS, _('In Process')), 
# 		(CONFIRMED, _('Confirmed')),
# 		(NO_MATCH, _('No match')),
# 		(PARTIAL_MATCH, _('partial match'))
# 	)

# 	SINGLE = 'single'
# 	POOL = 'pool'

# 	BET_TYPE_CHOICES = (
# 		(SINGLE, _('single')), 
# 		(POOL, _('pool')),
# 	)

# 	created_on = models.DateTimeField(auto_now_add=True,)
# 	payment = models.ForeignKey(Transaction, related_name='%(class)s_trans', on_delete=models.PROTECT)
# 	#player = models.ForeignKey(Player, related_name='%(class)s_player', on_delete=models.PROTECT)
# 	status = models.CharField(max_length=45, choices=BET_STATUS_CHOICES, default=IN_PROCESS)
# 	bet_type = models.CharField(max_length=45, choices=BET_TYPE_CHOICES,)
# 	history = HistoricalRecords(bases=[IPAddressHistoricalModel,], inherit=True)

# 	class Meta:
# 		abstract = True

# 	def __str__(self):
# 		return self.status


# class InterNationalBet(Bet):
# 	pot = models.ForeignKey(InterNationalPot, related_name='%(class)s_pot', on_delete=models.PROTECT)
# 	team = CountryField()
	
# 	def save(self, *args, **kwargs):
# 		self.full_clean()
# 		return super().save(*args, **kwargs)

# 	def clean(self):
# 		if not (self.team.pk == self.pot.team_1.pk or self.team.pk == self.pot.team_2.pk):
# 			raise ValidationError({'team': 'Team should belong to bet'})

# 	def __str__(self):
# 		return str(self.team)

# class ClubBet(Bet):
# 	pot = models.ForeignKey(ClubPot, related_name='%(class)s_pot', on_delete=models.PROTECT)
# 	team = models.ForeignKey(ClubTeam, related_name='%(class)s_team', on_delete=models.PROTECT)

# 	def save(self, *args, **kwargs):
# 		self.full_clean()
# 		return super().save(*args, **kwargs)

# 	def clean(self):
# 		if not (self.team.pk == self.pot.team_1.pk or self.team.pk == self.pot.team_2.pk):
# 			raise ValidationError({'team': 'Team should belong to bet'})

# 	def __str__(self):
# 		return str(self.team)

# class MapInterNationalBet(models.Model):

# 	bet_1 = models.ForeignKey(InterNationalBet, related_name='%(class)s_1_bet', on_delete=models.PROTECT)
# 	bet_2 = models.ForeignKey(InterNationalBet, related_name='%(class)s_2_bet', on_delete=models.PROTECT)
# 	amount = models.DecimalField(max_digits=10, decimal_places=2) 
# 	history = HistoricalRecords(bases=[IPAddressHistoricalModel,])

# 	def save(self, *args, **kwargs):
# 		self.full_clean()
# 		return super().save(*args, **kwargs)

# 	def clean(self):
# 		if self.bet_1.pk != self.pot.bet_2.pk :
# 			raise ValidationError('bet 1 and bet 2 should be different')

# 	def __str__(self):
# 		return str(self.amount)

# class MapClubBet(models.Model):

# 	bet_1 = models.ForeignKey(ClubBet, related_name='%(class)s_1_bet', on_delete=models.PROTECT)
# 	bet_2 = models.ForeignKey(ClubBet, related_name='%(class)s_2_bet', on_delete=models.PROTECT)
# 	amount = models.DecimalField(max_digits=10, decimal_places=2) 
# 	history = HistoricalRecords(bases=[IPAddressHistoricalModel,])

# 	def save(self, *args, **kwargs):
# 		self.full_clean()
# 		return super().save(*args, **kwargs)

# 	def clean(self):
# 		if self.bet_1.pk != self.pot.bet_2.pk :
# 			raise ValidationError('bet 1 and bet 2 should be different')

# 	def __str__(self):
# 		return str(self.amount)