import json
import os
import random
import redis

from django.utils import timezone
from django.conf import settings
from django import template
from django.core.cache import cache

from advertapp.models import Advert
from newsproject import settings

register = template.Library()


def zeroing_advert_counter(place):
	r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
	r.set(r.get(place), 0)
	return 0


def inc_advert_counter(place, advert_obj=None, set_advert=True):
	r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
	# yyyy_mm_dd|banner_name expire=30 days
	# когда закончится месяц, то сохранять предыдущие ключи в файл
	# пройти предыдущие 15 дней и сохранить в файл
	# ADVERT_STATIC_FILES_PATH хранить в медиа
	if set_advert:
		if not advert_obj:
			return 0
		advert_key = f'advert:{int(advert_obj.id)}:id'
		r.set(place, advert_key)
	advert_key = r.get(place)
	total_views = 0
	if advert_key:
		total_views = r.incr(advert_key)
	return total_views


@register.inclusion_tag('inc/advert_banner.html', takes_context=True)
def get_advert(context, place='skyscraper'):

	rez = cache.get(f'ads_{place}')
	if rez:
		inc_advert_counter(place, None, set_advert=False)
		return rez

	advert_qs = Advert.objects.for_show()
	advert_qs = advert_qs.filter(position=place)
	advert_obj = None
	if len(advert_qs):
		random_number = random.randint(0, len(advert_qs)-1)
		advert_obj = advert_qs[random_number]
	orientation = 'portrait'
	if place in ['content', 'top', 'bottom']:
		orientation = 'landscape'

	rez = {
		'advert_obj': advert_obj,
		'orientation': orientation,
	}

	cache.set(f'ads_{place}', rez, 60 * 5)  # 5 min

	return rez
