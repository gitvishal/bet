# from ..tasks import 
from .models.superpot import SuperPot
from django.utils import timezone

def start_pot_event(instance):
	if instance.is_active:
		sp = SuperPot.objects.filter(event=instance, status__in=[SuperPot.IN_PROCESS, SuperPot.OPEN_DECLAIRED])
		if not sp.exists():
			start_time = instance.start_time
			end_time = instance.start_time
			days = instance.days