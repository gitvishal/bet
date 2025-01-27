from master.viewsets.views import (RegistrationView as BaseRegistrationView, 
	RegistrationURLView as BaseRegistrationURLView)
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from django.core.signing import dumps
from master.models import User, Manager
from django.urls import reverse_lazy
from .forms import RegistrationURLForm

class RegistrationView(BaseRegistrationView):
	one_to_one_model = Manager
	parent_model = User
	success_url = reverse_lazy('master:users:manager:home')

	def extract_data(self):
		parent_user, payload = super().extract_data()
		if not self.admin.is_superuser:
			raise PermissionDenied(
				'link is not generated by admin'
				'Only admin credentials can generate manager link'
			)
		return parent_user, payload

class RegistrationURLView(BaseRegistrationURLView):
	form_class = RegistrationURLForm
	template_name = 'master/manager/registration_form_email.html'
	success_url = reverse_lazy('master:users:manager:home')

class HomeView(TemplateView):
	template_name = 'index.html'

