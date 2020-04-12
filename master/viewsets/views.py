from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site 
from django.views.generic.edit import FormView
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from django.views.generic import TemplateView, View, RedirectView
from .forms import AgentRegistrationURLForm, RegistrationURLForm, UserCreationForm
from master.models import User, Agent
from django.core.exceptions import DisallowedHost, PermissionDenied
from master.utils.queryset import get_instance_or_none
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import DisallowedHost, PermissionDenied
from django.contrib.auth import get_user_model
User = get_user_model()

class HomeView(TemplateView):
	template_name = 'index.html'

class ManagementHomeView(TemplateView):
	template_name = 'master/management_home.html'

@method_decorator([login_required(login_url=settings.LOGIN_URL),], name='dispatch')
class HomeRemoteRedirectView(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		if self.request.user.is_superuser and self.request.user.user_type == User.ADMIN:
			return reverse_lazy('admin:index')
		elif self.request.user.user_type == User.SUPERVISOR:
			return reverse_lazy('users:supervisor:home')
		elif self.request.user.user_type == User.EMPLOYEE:
			return reverse_lazy('users:employee:home')
		elif self.request.user.user_type == User.MANAGER:
			return reverse_lazy('users:manager:home')
		elif self.request.user.user_type in [User.SUB_AGENT, User.AGENT]:
			return reverse_lazy('users:agent:home')
		elif self.request.user.user_type == User.ONLINE_PLAYER:
			return reverse_lazy('users:onlineplayer:home')
		else:
			return reverse_lazy('users:index')

class RegistrationView(BaseRegistrationView):
	model = User
	form_class = UserCreationForm
	registration_path = None

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'token': self.token})
		return kwargs

	def post(self, request, token, *args, **kwargs):
		self.token = token
		return super().post(request, *args, **kwargs)

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
			'user_email' : form.cleaned_data['email'],
			'user_type' : form.cleaned_data['user_type'],
		}

	def form_valid(self, form):
		context = self.email_context(form)
		token = dumps(context)
		context['token'] = token
		context['site'] = get_current_site(self.request)
		context['site_name'] = 'Online Betting',
		context['activation_url'] = reverse_lazy(self.registration_path, kwargs={'token':token})
		subject = 'Registration form for site {site}'.format(**context)
		form.send_email(subject, render_to_string(self.email_template_name, context=context))
		return super().form_valid(form)

class AgentRegistrationURLView(RegistrationURLView):
	form_class = AgentRegistrationURLForm
	title = _('Form to Send Email For Registration as Agent')
	registration_path = 'users:agent:registration'

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({
			'user_type_choices': [(User.AGENT, 'agent'),],
		})
		return kwargs

	def email_context(self, form):
		context = super().email_context(form)
		agent = get_instance_or_none(Agent, user=self.request.user)

		context['parent'] = {
			'module': User.__module__, 'model':User.__name__, 
			'params':{'email':self.request.user.email, 'user_type': self.request.user.user_type,}
		}
		context['child'] = {
			'module': Agent.__module__, 'model':Agent.__name__,
			'parent_agent': {'pk':agent and agent.pk, 'agent_parent_param': 'parent_node'},
			'params':{
				'designation': form.cleaned_data['designation'], 
				'commission':form.cleaned_data['commission'],
			}
		}
		return context
