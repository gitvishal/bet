from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords
from simple_history import register as history_register
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from jsonfield import JSONField
from django_cryptography.fields import encrypt
import uuid

class IPAddressHistoricalModel(models.Model):
	ip_address = models.GenericIPAddressField(_('IP address'))

	class Meta:
		abstract = True

class User(AbstractUser):

	MANAGER = 1
	SUPERVISOR = 2
	ADMIN = 3
	EMPLOYEE = 4
	AGENT = 5
	SUB_AGENT = 6
	ONLINE_PLAYER = 7

	ROLE_CHOICES = (
		(MANAGER, 'manager'),
		(SUPERVISOR, 'supervisor'),
		(EMPLOYEE, 'employee'),
		(ADMIN, 'admin'),
		(AGENT, 'agent'),
		(ONLINE_PLAYER, 'online player'),
		(SUB_AGENT, 'sub agent'),
	)

	ALL_STAFF_USER = [MANAGER, SUPERVISOR, ADMIN, EMPLOYEE]
	ALL_AGENTS = [AGENT, SUB_AGENT]

	PERMISSION_USER_CREATION = {
		ADMIN: [(MANAGER, 'manager'),],
		MANAGER: [(SUPERVISOR, 'supervisor'),],
		SUPERVISOR: [(EMPLOYEE, 'employee'),],
		AGENT:[(SUB_AGENT, 'sub agent'),],
		SUB_AGENT:[(SUB_AGENT, 'sub agent'),],
	}

	user_type = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
	username = PhoneNumberField(_('mobile'), unique=True, 
		error_messages={
			'unique': _("A user with that mobile already exists."),
		},
	)
	history = HistoricalRecords(bases=[IPAddressHistoricalModel,])

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ('email',)

	def save(self, *args, **kwargs):
		if self.is_superuser:
			self.user_type = __class__.ADMIN
		super().save(*args, **kwargs)

class UserProfile(models.Model):
	designation = models.CharField(max_length=70, default='no designation')
	bank_details = encrypt(RichTextField(blank=True, null=True))
	history = HistoricalRecords(bases=[IPAddressHistoricalModel,], inherit=True)

	class Meta:
		abstract = True

	def __str__(self):
		return str(self.designation)

class Manager(UserProfile):
	PARENT_USER_TYPE = User.ADMIN
	user = models.OneToOneField(User, related_name='%(class)s_manager', 
		on_delete=models.PROTECT, verbose_name=_('Manager'),
		limit_choices_to={'user_type': User.MANAGER})
	parent = models.OneToOneField(User, related_name='%(class)s_admin', 
		on_delete=models.PROTECT, verbose_name=_('Admin'), 
		limit_choices_to={'is_superuser':True, 'user_type': User.ADMIN})

	class Meta:
		permissions = (
			("can_create_superpot", "can create superpot"),
			("can_update_superpot", "can update superpot"),
			("can_delete_superpot", "can delete superpot"),
			("can_manage_user", "can manage user"),
			("can_manage_bank_details", "can manage bank details"),
		)
	
class Supervisor(UserProfile): 
	PARENT_USER_TYPE = User.MANAGER
	user = models.OneToOneField(User, related_name='%(class)s_supervisor', 
		on_delete=models.PROTECT, verbose_name=_('Supervisor'),
		limit_choices_to={'user_type': User.SUPERVISOR})
	parent = models.ForeignKey(Manager, related_name='%(class)s_manager', 
		on_delete=models.PROTECT, verbose_name=_('Manager'),
		limit_choices_to={'user_type': User.MANAGER})

	class Meta:
		permissions = (
			("can_create_superpot", "can create superpot"),
			("can_update_superpot", "can update superpot"),
			("can_delete_superpot", "can delete superpot"),
			("can_manage_user", "can manage user"),
			("can_manage_bank_details", "can manage bank details"),
		)

class Employee(UserProfile):
	PARENT_USER_TYPE = User.SUPERVISOR
	user = models.OneToOneField(User, related_name='%(class)s_employee', 
		on_delete=models.PROTECT, verbose_name=_('Employee'),
		limit_choices_to={'user_type': User.EMPLOYEE})
	parent = models.ForeignKey(Supervisor, related_name='%(class)s_supervisor', 
		on_delete=models.PROTECT, verbose_name=_('Supervisor'),
		limit_choices_to={'user_type': User.SUPERVISOR})

	class Meta:
		permissions = (
			("can_create_superpot", "can create superpot"),
			("can_update_superpot", "can update superpot"),
			("can_delete_superpot", "can delete superpot"),
			("can_manage_user", "can manage user"),
			("can_manage_bank_details", "can manage bank details"),
		)

class OnlinePlayer(UserProfile):
	user = models.OneToOneField(User, related_name='%(class)s_player', 
		on_delete=models.PROTECT, verbose_name=_('Player'),
		limit_choices_to={'user_type': User.ONLINE_PLAYER})
	monitoring_user = models.OneToOneField(User, related_name='%(class)s_player', 
		on_delete=models.PROTECT, verbose_name=_('Player'),
		limit_choices_to={'user_type__in': User.ALL_STAFF_USER})

class Agent(UserProfile):
	parent = models.ForeignKey(User, related_name='%(class)s_player', 
		on_delete=models.PROTECT, verbose_name=_('Refered by'),
		limit_choices_to={'user_type__in': User.ALL_STAFF_USER + User.ALL_AGENTS})
	user = models.OneToOneField(User, related_name='%(class)s_agent', 
		on_delete=models.PROTECT, verbose_name=_('Agent'),
		limit_choices_to={'user_type__in': User.ALL_AGENTS})
	commission = models.FloatField(validators=[MinValueValidator(5), MaxValueValidator(50)],)
	parent_node = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')

	class Meta:
		permissions = (
			("can_manage_child_node", "can manage child node"),
		)

	class MPTTMeta:
		order_insertion_by = ('user',)

	def __str__(self):
		return str(self.user)

class AgentPlayer(models.Model):
	agent = models.ForeignKey(Agent, related_name='%(class)s_agent', on_delete=models.PROTECT)
	name = models.CharField(max_length=60)
	mobile = PhoneNumberField(blank=True, null=True)
	created_on = models.DateTimeField(auto_now_add=True,)
	history = HistoricalRecords(bases=[IPAddressHistoricalModel,])

	def __str__(self):
		return str(self.agent)