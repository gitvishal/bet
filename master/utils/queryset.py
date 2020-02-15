from django.utils.translation import ugettext_lazy as _

def get_instance_or_none(model, **parameters):
	try:
		instance = model.objects.get(**parameters)
	except model.DoesNotExist as e:
		instace = None
	return instance