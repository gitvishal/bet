from django import forms
from master.models import User, OnlinePlayer
from django.db import transaction
from registration.forms import RegistrationFormUniqueEmail

class RegistrationForm(RegistrationFormUniqueEmail):
	class Meta(RegistrationFormUniqueEmail.Meta):
		model = User

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.user_type = User.ONLINE_PLAYER
		user.save()
		OnlinePlayer.objects.create(user=user, designation='online player')
		return user