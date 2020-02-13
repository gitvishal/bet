from django.shortcuts import redirect, render
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from django.views.generic import TemplateView
from django.utils import timezone
from master.viewsets.forms import RegistrationForm
from django.core import signing
from django.db import transaction
from master.models import User, Agent
from django.core.signing import loads, SignatureExpired
from django.urls import reverse_lazy
from django.core.exceptions import DisallowedHost, PermissionDenied

class AgentRegistrationView(BaseRegistrationView):
	model = User
	form_class = RegistrationForm
	success_url = reverse_lazy('master:users:agent:home')

	def extract_data(self):
		try:
			payload = loads(self.token, max_age=timezone.timedelta(hours=8))
			if payload['parent_user_type'] not in User.ALL_STAFF_USER:
				raise PermissionDenied('parent user is not one of the staff') from e

			parent_user = User.objects.get(email=payload['email'], 
				user_type=payload['parent_user_type'])

		except User.DoesNotExist as e:
			raise PermissionDenied('parent user Does Not Exist') from e
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
		user.user_type = User.AGENT
		user.save()
		Agent.objects.create(user=user, parent=parent_user, 
			designation='Direct Agent', commission=payload['commission'])
		return user

class SubAgentRegistrationView(BaseRegistrationView):
	model = User
	form_class = RegistrationForm
	success_url = reverse_lazy('master:users:agent:home')

	def extract_data(self):
		try:
			payload = loads(self.token, max_age=timezone.timedelta(hours=8))
			if payload['parent_user_type'] not in [User.AGENT, User.SUB_AGENT]:
				raise PermissionDenied('for sub agent parent must be agent or subagent') from e
				
			parent_user = User.objects.get(email=payload['email'], 
				user_type=payload['parent_user_type'])

		except User.DoesNotExist as e:
			raise PermissionDenied('parent user Does Not Exist') from e
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
		user.user_type = User.SUB_AGENT
		user.save()
		parent = Agent.objects.get(user=parent_user)
		Agent.objects.create(user=user, parent=parent_user, 
			designation='Sub Agent', commission=payload['commission'], parent_node=parent)
		return user

class HomeView(TemplateView):
	template_name = 'index.html'