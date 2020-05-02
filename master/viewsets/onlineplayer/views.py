from django.shortcuts import redirect, render
from registration.backends.default.views import RegistrationView as BaseRegistrationView
from django.views.generic import TemplateView, DetailView, FormView
from .forms import RegistrationForm, BankDetails
from django.urls import reverse_lazy
from .permissions import PermissionMixin
from .tables import BalanceAccountTable
from master.models import OnlinePlayer, OnlinePlayerBalanceAccount
from django.db.models import Sum, Case, When, Q, F, DecimalField, Value
from django.contrib.auth import get_user_model
from table.views import FeedDataView
User = get_user_model()

class RegistrationView(BaseRegistrationView):
	model = User
	form_class = RegistrationForm
	success_url = reverse_lazy('users:onlineplayer:auth_login')

class OnlinePlayerContextMixin(PermissionMixin):

	def get_object(self):
		return OnlinePlayer.objects.get(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		balance = OnlinePlayerBalanceAccount.objects.filter(player=self.object, 
			transaction__status=Transaction.SUCCESS,
			).annotate(
				amount=Case(
					When(
						Q(transaction_type=OnlinePlayerBalanceAccount.DEBIT),
						then=F('transaction__amount') * -1
					),
					When(
						Q(transaction_type=OnlinePlayerBalanceAccount.CREDIT),
						then=F('transaction__amount')
					),
					default=Value(0), 
					output_field=DecimalField(),
				)
			)
		context['balance'] = balance.aggregate(amount=Sum('amount'))['amount']
		context['table'] = BalanceAccountTable(OnlinePlayerBalanceAccount.objects.filter(player=self.object))
		context['bank_form'] = BankDetails(initial=self.object.bank_details or {})
		return context

class HomeView(OnlinePlayerContextMixin, DetailView):
	template_name = 'online_player/home.html'

class AccountView(OnlinePlayerContextMixin, DetailView):
	template_name = 'online_player/account.html'

class BankFormView(OnlinePlayerContextMixin, FormView):
	success_url = reverse_lazy('users:onlineplayer:transaction')
	template_name = 'online_player/account.html'

	def form_valid(self, form):
		self.object.bank_details = form.cleaned_data
		self.object.save()
		return super().form_valid(form)

class AccountFeedDataView(FeedDataView):
	token = BalanceAccountTable.token

	def get_queryset(self):
		player = OnlinePlayer.objects.get(user=self.request.user)
		return super().get_queryset().filter(player=player)

