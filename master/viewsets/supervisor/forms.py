from master.viewsets.forms import RegistrationURLForm as BaseRegistrationURLForm
from django import forms
from master.models import User

class RegistrationURLForm(BaseRegistrationURLForm):
	user_type = forms.ChoiceField(choices=User.PERMISSION_USER_CREATION[User.SUPERVISOR])