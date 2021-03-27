import random

from django import template

from advertapp.models import Advert

register = template.Library()


@register.inclusion_tag('inc/advert_banner.html', takes_context=True)
def get_advert(context, place='skyscraper'):

	advert_qs = Advert.objects.for_show()
	advert_qs = advert_qs.filter(position=place)
	advert_obj = None
	if len(advert_qs):
		random_number = random.randint(0, len(advert_qs)-1)
		advert_obj = advert_qs[random_number]
	orientation = 'portrait'
	if place in ['content', 'top', 'bottom']:
		orientation = 'landscape'

	return {
		'advert_obj': advert_obj,
		'orientation': orientation,
	}
