from table import Table
from table.columns import Column, DatetimeColumn, LinkColumn, Link
from table.utils import A, mark_safe, escape
from django.urls import reverse_lazy
from master.models.payments import OnlinePlayerBalanceAccount, Transaction, BalanceAccount
from django.utils.translation import ugettext_lazy as _


def pill_batch(status):
	return {
		Transaction.INPROCESS:mark_safe('<span class="badge badge-pill badge-primary">Waiting for Approve</span>'),
		Transaction.SUCCESS:mark_safe('<span class="badge badge-pill badge-success">Success</span>'),
		Transaction.FAILED:mark_safe('<span class="badge badge-pill badge-danger">Failed</span>'),
		BalanceAccount.CREDIT:mark_safe('<span class="badge badge-pill badge-dark">Credit <span class="badge badge-light">+</span></span>'),
		BalanceAccount.DEBIT:mark_safe('<span class="badge badge-pill badge-dark">Debit <span class="badge badge-light">-</span></span>'),
		
	}.get(status, escape(status))

class StatusColumn(Column):
	def render(self, obj):
		return pill_batch(A(self.field).resolve(obj))

class AmountColumn(Column):
	def render(self, obj):
		return mark_safe('<span class="badge badge-light">%s</span>' %(A(self.field).resolve(obj)))


class BalanceAccountTable(Table):
	transaction = LinkColumn(field='transaction.transaction_id', header=_('Transaction ID'),
		links=[
			Link(text=A('transaction.transaction_id'), 
				viewname='', args=(A('transaction.pk'),), attrs={'target':'_blank'},),
		],
		sortable=False, searchable=False, 
	)
	created_on = DatetimeColumn(field='created_on', header=_('Transaction Entry Date'))
	transaction_type = StatusColumn(field='transaction_type', header=_('Transaction Type'))
	amount = AmountColumn(field='transaction.amount', header=_('Amount'))
	status = StatusColumn(field='transaction.status', header=_('Status'))

	class Meta:
		model = OnlinePlayerBalanceAccount
		ajax = True
		ajax_source = reverse_lazy('users:onlineplayer:transaction')