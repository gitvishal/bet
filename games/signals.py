from django.db.models.signals import post_save, pre_save, pre_delete
from django.db import IntegrityError, transaction
from django.dispatch import receiver
from .models import SuperPotEvent
from .utils.async import start_pot_event

@receiver(post_save, sender=SuperPotEvent)
def superpot_event_trigger(sender, instance, created, **kwargs):
	transaction.on_commit(lambda: start_pot_event(sender, instance, created, **kwargs)) 