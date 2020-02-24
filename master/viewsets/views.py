from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site 
from django.views.generic.edit import FormView
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from django.views.generic import TemplateView
from django.utils import timezone
from .forms import AgentRegistrationURLForm, RegistrationURLForm, UserCreationForm
from django.core import signing
from django.db import transaction
from master.models import User, Agent
from django.core.signing import loads, SignatureExpired, dumps
from django.core.exceptions import DisallowedHost, PermissionDenied
from master.utils.queryset import get_instance_or_none
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
import sys

class RegistrationView(BaseRegistrationView):
	model = User
	form_class = UserCreationForm
	one_to_one_model = None
	success_url = None
	registration_path = None

	def extract_data(self):

		try:
			payload = loads(self.token, max_age=timezone.timedelta(hours=8))
		except SignatureExpired as e:
			raise DisallowedHost("Link is expired. Request a new link") from e

		parent_payload = payload['parent']
		ParentModel = getattr(sys.modules[parent_payload['module']], parent_payload['model'])

		try:
			parent = ParentModel.objects.get(**parent_payload['params'])

		except ParentModel.DoesNotExist as e:
			raise PermissionDenied('Super user Does Not Exist') from e
		return parent, payload

	def post(self, request, token, *args, **kwargs):
		self.token = token
		return super().post(request, *args, **kwargs)

	@transaction.atomic
	def register(self, form):
		parent, payload = self.extract_data()
		child_payload = payload['child']
		user = super().register(form)
		user.user_type = payload['user_type']
		user.email = payload['user_email']
		user.save()
		ChildModel = getattr(sys.modules[child_payload['module']], child_payload['model'])
		ChildModel.objects.create(user=user, parent=parent, **child_payload['params'])
		return user

class RegistrationURLView(FormView):
	form_class = RegistrationURLForm
	email_template_name = 'master/email/activation_email.html'
	template_name = 'master/registration_form_email.html'
	title = _('Send Email For Registration')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = self.title
		return context

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({
			'user_type_choices': User.PERMISSION_USER_CREATION[self.request.user.user_type]
		})
		return kwargs

	def email_context(self, form):
		return {
			'site' : get_current_site(self.request).name,
			'user_email' : form.cleaned_data['email'],
			'user_type' : form.cleaned_data['user_type'],
		}

	def form_valid(self, form):
		context = self.email_context(form)
		token = dumps(context)
		context['token'] = token
		context['activation_url'] = reverse_lazy(self.registration_path, kwargs={'token':token})
		subject = 'Registration form for site {site}'.format(**context)
		form.send_email(subject, render_to_string(self.email_template_name, context=context))
		return super().form_valid(form)

class AgentRegistrationURLView(RegistrationURLView):
	form_class = AgentRegistrationURLForm
	title = _('Form to Send Email For Registration as Agent')
	registration_path = 'master:users:agent:registration'

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({
			'user_type_choices': [(User.AGENT, 'agent'),],
		})
		return kwargs

	def email_context(self, form):
		context = super().email_context(form)
		try:
			agent = Agent.objects.get(user=self.request.user).pk
		except Agent.DoesNotExist:
			agent = None 

		context['parent'] = {
			'module': User.__module__, 'model':User.__name__, 
			'params':{'email':self.request.user.email, 'user_type': self.request.user.user_type,}
		}
		context['child'] = {
			'module': Agent.__module__, 'model':Agent.__name__,
			'params':{
				'designation': form.cleaned_data['designation'], 
				'commission':form.cleaned_data['commission'],
				'parent_node': agent,
			}
		}
		return context