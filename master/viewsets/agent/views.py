from django.shortcuts import redirect, render
from master.viewsets.views import (RegistrationView as BaseRegistrationView, 
	RegistrationURLView as BaseRegistrationURLView)
from registration.backends.default.views import RegistrationView as SuperBaseRegistrationView
from django.views.generic import TemplateView
from django.core.signing import loads, SignatureExpired, dumps
from django.core.exceptions import DisallowedHost, PermissionDenied
from master.utils.queryset import get_instance_or_none
from django.db import transaction
from master.models import User, Agent
from django.urls import reverse_lazy

class RegistrationView(BaseRegistrationView):
	one_to_one_model = Agent
	parent_model = User
	success_url = reverse_lazy('master:users:agent:home')

	def extract_data(self):
		try:
			payload = loads(self.token, max_age=timezone.timedelta(hours=8))
			parent_user = self.parent_model.objects.get(
				user__email=payload['parent_email'], 
				user__user_type=payload['parent_user_type']
			)
			if not parent_user.user_type in User.ALL_STAFF_USER + User.ALL_AGENTS:
				raise PermissionDenied('Super user Does Not Exist')

		except self.parent_model.DoesNotExist as e:
			raise PermissionDenied('Super user Does Not Exist') from e
		except SignatureExpired as e:
			raise DisallowedHost("Link is expired. Request a new link") from e
		return parent_user, payload

	@transaction.atomic
	def register(self, form):
		parent_user, payload = self.extract_data()
		user = super(SuperBaseRegistrationView, self).register(form)
		user.user_type = payload['user_type']
		user.email = payload['user_email']
		user.save()
		agent = self.one_to_one_model.objects.create(user=user, parent=parent_user, 
			designation=payload['designation'], commission=payload['commission'])
		if parent_user.user_type in User.ALL_AGENTS + User.ALL_STAFF_USER:
			parent_node = self.one_to_one_model.objects.get(user=parent_user)
			agent.parent_node = parent_node
			agent.save()
		return user

class HomeView(TemplateView):
	template_name = 'index.html'