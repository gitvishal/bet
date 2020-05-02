from django import forms
from master.models import OnlinePlayer
from django.db import transaction
from registration.forms import RegistrationFormUniqueEmail
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationForm(RegistrationFormUniqueEmail):
	class Meta(RegistrationFormUniqueEmail.Meta):
		model = User

	@property
	def monitoring_user(self):
		users = User.objects.filter(user_type__in=User.ALL_STAFF_USER).values('onlineplayer_moniter__pk', 'pk')
		users = users.annotate(online_user_count=Count('onlineplayer_moniter'))
		return User.objects.get(pk=users.order_by('online_user_count')[0]['pk'])

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.user_type = User.ONLINE_PLAYER
		user.save()
		OnlinePlayer.objects.create(user=user, designation='online player', monitoring_user=self.monitoring_user)
		return user

class BankDetails(forms.Form):
	full_name = forms.CharField(label=_('The Account Holders Name'), max_length=100, help_text=_('Name as per account'))
	account = forms.CharField(label=_('Account Number'), max_length=100, help_text=_('Account number'))
	iban = forms.CharField(label=_('IBAN'), max_length=100, help_text=_('add None if not known'))
	bank_name = forms.CharField(label=_('Bank Name'), max_length=100, help_text=_('Bank Name'))
	bank_address = forms.CharField(label=_('Bank Address'), max_length=100, help_text=_('Bank adddress'))
	sort_code = forms.CharField(label=_('Sort Code'), max_length=100, help_text=_('add None if not known'))
	rout_number = forms.CharField(label=_('Routing Number'), max_length=100, help_text=_('add None if not known'))
	s_code = forms.CharField(label=_('SWIFT/BIC Code'), max_length=100, help_text=_('add None if not known'))
	ifsc = forms.CharField(label=_('IFSC Code'), max_length=100, help_text=_('add None if not known'))
	routing_code = forms.CharField(label=_('Routing Code'), max_length=100, help_text=_('add None if not known'))
