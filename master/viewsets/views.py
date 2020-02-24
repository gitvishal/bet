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
from master.models import User
from django.core.signing import loads, SignatureExpired, dumps
from django.core.exceptions import DisallowedHost, PermissionDenied
from master.utils.queryset import get_instance_or_none
from django.urls import reverse_lazy

class RegistrationView(BaseRegistrationView):
	model = User
	form_class = UserCreationForm
	one_to_one_model = None
	parent_model = None
	success_url = None
	registration_path = None

	def extract_data(self):
		try:
			payload = loads(self.token, max_age=timezone.timedelta(hours=8))
			parent_user = self.parent_model.objects.get(
				user__email=payload['parent_email'], 
				user__user_type=payload['parent_user_type']
			)

		except self.parent_model.DoesNotExist as e:
			raise PermissionDenied('Super user Does Not Exist') from e
		except SignatureExpired as e:
			raise DisallowedHost("Link is expired. Request a new link") from e
		return parent_user, payload

	def post(self, request, token, *args, **kwargs):
		self.token = token
		return super().post(request, *args, **kwargs)

	@transaction.atomic
	def register(self, form):
		parent_user, payload = self.extract_data()
		user = super().register(form)
		user.user_type = payload['user_type']
		user.email = payload['user_email']
		user.save()
		self.one_to_one_model.objects.create(user=user, parent=parent_user, designation=payload['designation'])
		return user

class RegistrationURLView(FormView):
	form_class = RegistrationURLForm
	email_template_name = 'master/email/activation_email.html'
	template_name = 'master/registration_form_email.html'

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({
			'user_type_choices': User.PERMISSION_USER_CREATION[self.request.user.user_type]
		})
		return kwargs

	def email_context(self, form):
		return {
			'site' : get_current_site(self.request).name,
			'parent_email' : self.request.user.email,
			'parent_user_type' : self.request.user.user_type,
			'user_email' : form.cleaned_data['email'],
			'designation' : form.cleaned_data['designation'],
			'user_type' : form.cleaned_data['user_type'],
		}

	def form_valid(self, form):
		context=self.email_context(form)
		token = dumps(context)
		context['token'] = token
		context['activation_url'] = reverse_lazy(self.registration_path, kwargs={'token':token})
		subject = 'Registration form for site {site}'.format(**context)
		form.send_email(subject, render_to_string(self.email_template_name, context=context))
		return super().form_valid(form)

class AgentRegistrationURLView(RegistrationURLView):
	form_class = AgentRegistrationURLForm

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({
			'user_type_choices': [(User.AGENT, 'agent'),],
		})
		return kwargs
	
	def email_context(self, form):
		context = super().email_context(form)
		context['commission'] = form.cleaned_data['commission']
		return context