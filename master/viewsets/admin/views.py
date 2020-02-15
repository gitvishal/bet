from master.viewsets.views import (RegistrationView as BaseRegistrationView, 
	RegistrationURLView as BaseRegistrationURLView)
from master.models import User, Manager
from .forms import RegistrationURLForm

class RegistrationURLView(BaseRegistrationURLView):
	form_class = RegistrationURLForm
	success_url = reverse_lazy('admin:index')
