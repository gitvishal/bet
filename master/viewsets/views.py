from django.shortcuts import redirect, render
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from django.views.generic import TemplateView
from django.utils import timezone
from .forms import RegistrationForm
from django.core import signing
from django.db import transaction
from master.models import User
from django.core.signing import loads, SignatureExpired
from django.core.exceptions import DisallowedHost, PermissionDenied

class RegistrationView(BaseRegistrationView):
	model = User
	form_class = RegistrationForm
	one_to_one_model = None
	success_url = None

	def extract_data(self):
		try:
			payload = loads(self.token, max_age=timezone.timedelta(hours=8))
			parent_user = User.objects.get(email=payload['email'], user_type=payload['parent_user_type'])

		except User.DoesNotExist as e:
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
		user.save()
		self.one_to_one_model.objects.create(user=user, parent=parent_user, designation=payload['designation'])
		return user


# from django.shortcuts import render
# from django.views.generic import View, RedirectView
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from django.urls import reverse_lazy
# from django.core.exceptions import PermissionDenied

# @method_decorator([login_required(login_url=settings.LOGIN_URL),], name='dispatch')
# class RegistrationRemoteRedirectView(RedirectView):
# 	def get_redirect_url(self, *args, **kwargs):
# 		if self.request.user.is_superuser:
# 			return reverse_lazy('admin:index')
# 		elif self.request.user.remoteuser.user_type.user_role == 'STUDENT':
# 			return reverse_lazy('student:index')
# 		elif self.request.user.remoteuser.user_type.user_role == 'FACULTY':
# 			return reverse_lazy('faculty:index')
# 		elif self.request.user.remoteuser.user_type.user_role == 'CO-ORDINATOR':
# 			return reverse_lazy('coordinator:index')
# 		elif self.request.user.remoteuser.user_type.user_role == 'CORPORATE-CLIENT':
# 			return reverse_lazy('corporate_client:index')
# 		elif self.request.user.remoteuser.user_type.user_role == 'MASTER-CO-ORDINATOR':
# 			return reverse_lazy('master_coordinator:index')
# 		else:
# 			raise PermissionDenied