from django.db import models
from phonenumber_field.modelfields import PhoneNumberField as BasePhoneNumberField
from phonenumber_field.formfields import PhoneNumberField  as PhoneNumberFormField
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _

class PhoneNumberField(BasePhoneNumberField):
	def formfield(self, **kwargs):
		defaults = {
			"form_class": PhoneNumberFormField,
			"error_messages": self.error_messages,
		}
		defaults.update(kwargs)
		return super(models.CharField, self).formfield(**defaults)

class IPAddressHistoricalModel(models.Model):
	ip_address = models.GenericIPAddressField(_('IP address'), blank=True, null=True)

	class Meta:
		abstract = True

class HistoricalModels(models.Model):
	history = HistoricalRecords(bases=[IPAddressHistoricalModel,], inherit=True)

	class Meta:
		abstract = True