from django import forms
from master.models import User
from django.core.mail import EmailMessage
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from master.utils.queryset import get_instance_or_none
from registration.forms import RegistrationFormUniqueEmail
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class RegistrationForm(RegistrationFormUniqueEmail):
	class Meta(RegistrationFormUniqueEmail.Meta):
		model = User

class RegistrationURLForm(forms.Form):
	email = forms.EmailField(label=_('Email to register'))
	designation = forms.CharField(label=_('Role'))
        
	def __init__(self, *args, **kwargs):
		user_type_choices = kwargs.pop('user_type_choices')
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Send Email'))
		self.fields['user_type'] = forms.ChoiceField(label=_('Register As'), choices=user_type_choices)

	def clean_email(self):
		email = self.cleaned_data['email']
		if get_instance_or_none(User, email=email):
			raise forms.ValidationError(_('This email is already a registered user'))
		return email

	def send_email(self, subject, html_content):
		msg = EmailMessage(subject, html_content, [self.cleaned_data['email']])
		msg.content_subtype = "html"
		msg.send(failed_silently=True)

class AgentRegistrationURLForm(RegistrationURLForm):
	commission = forms.FloatField(label=_('commission in percentage'), 
		validators=[MinValueValidator(5), MaxValueValidator(50)])
	designation = forms.CharField(label=_('Role'), initial="Agent")

	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.fields['designation'].initial = 'Agent'
	# 	self.fields['designation'].widget = forms.HiddenInput

		