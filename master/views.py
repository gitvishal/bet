from django.shortcuts import render 
from django.views.generic import View, RedirectView, TemplateView
from django.core.exceptions import DisallowedHost, PermissionDenied
from master.utils.queryset import get_instance_or_none
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class HomeView(TemplateView):
	template_name = 'index.html'


@method_decorator([login_required(login_url=settings.LOGIN_URL),], name='dispatch')
class HomeRemoteRedirectView(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		if self.request.user.is_superuser and self.request.user.user_type == User.ADMIN:
			return reverse_lazy('admin:index')
		elif self.request.user.user_type == User.SUPERVISOR:
			return reverse_lazy('master:users:supervisor:home')
		elif self.request.user.user_type == User.EMPLOYEE:
			return reverse_lazy('master:users:employee:home')
		elif self.request.user.user_type == User.MANAGER:
			return reverse_lazy('master:users:manager:home')
		elif self.request.user.user_type in [User.SUB_AGENT, User.AGENT]:
			return reverse_lazy('master:users:agent:home')
		elif self.request.user.user_type == User.ONLINE_PLAYER:
			return reverse_lazy('master:users:onlineplayer:home')
		else:
			raise PermissionDenied
