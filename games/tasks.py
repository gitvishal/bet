from celery import shared_task
from .models.superpot import SuperPot

@shared_task
def pot_start_event(instance):
	sp = SuperPot.objects.filter(event=instance, status__in=[SuperPot.IN_PROCESS, SuperPot.OPEN_DECLAIRED])
	if not sp.exists():
		start_time = instance.start_time
		days = instance.days
	return func(sf_api_obj, instance, serializer, log_model, log_param, serializer_fields) 



# def saleforce_async_api(sf_api_obj, instance, serializer, log_model, log_param, serializer_fields=None, seconds=5):
# 	job = api_call.apply_async(
# 		(sf_api, sf_api_obj, instance, serializer, log_model, log_param, serializer_fields),
# 		eta=timezone.localtime(timezone.now()) + timezone.timedelta(seconds=seconds)
# 		# queue='saleforce', #using default queue can change if you want
# 		# countdown=10 # not yet decided
# 	)