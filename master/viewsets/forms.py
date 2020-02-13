from django import forms
from master.models import User
from registration.forms import RegistrationFormUniqueEmail

class RegistrationForm(RegistrationFormUniqueEmail):
	class Meta(RegistrationFormUniqueEmail.Meta):
		model = User