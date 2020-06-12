from django import template
from django.contrib.auth.models import User
from django.utils import timezone

from newsproject.defaults import RACK
from postapp.models import Post

register = template.Library()


@register.inclusion_tag('inc/main_menu.html', takes_context=True)
def get_main_menu(context):
	"""
	Выводит виджет меню
	"""
	get_keys = list(context.request.GET.keys())
	active = context.dicts[3].get('active', None)
	if len(get_keys) == 1:
		active = context.request.GET.get(get_keys[0], None)

	return {
		'active': active,
		'main_menu': RACK.get('main_menu', None),
		'site_name': RACK.get('site_name', None),
	}


@register.inclusion_tag('inc/footer.html', takes_context=True)
def get_footer(context):
	"""
	Выводит виджет футера
	"""
	return {
		'site_name': RACK.get('site_name', None),
	}


@register.inclusion_tag('inc/tags.html', takes_context=True)
def get_tags(context):
	user = None
	show_count = False
	user_qs = User.objects.filter(username=context.get('user'))
	if user_qs.count() == 1:
		user = user_qs[0]
		show_count = user.is_staff
	tag_typle = Post.objects.for_user(user).values_list('tags__name', 'tags__slug')
	tag_dct = dict()
	for tag in tag_typle:
		if tag[1] and '0' not in tag[1]:
			tag_dct.setdefault(tag[1], {'name': tag[0], 'count': 0})
			tag_dct[tag[1]]['count'] += 1
	return {
		'tag_dct': tag_dct,
		'show_count': show_count,
	}


@register.inclusion_tag('inc/calendar.html', takes_context=True)
def get_calendar(context):
	user = None
	user_qs = User.objects.filter(username=context.get('user'))
	if user_qs.count() == 1:
		user = user_qs[0]
	post_qs = Post.objects.for_user(user)
	date_dct = dict()
	date_format = "%B %Y"
	date_format_slug = "%Y-%m"
	for post in post_qs:
		date_post = post.date_post.strftime(date_format)
		date_post_slug = post.date_post.strftime(date_format_slug)
		date_dct.setdefault(date_post_slug, {'name': date_post, 'count': 0})
		date_dct[date_post_slug]['count'] += 1
	return {
		'date_dct': date_dct,
	}


@register.inclusion_tag('inc/recent.html', takes_context=True)
def get_recent(context):
	"""
	Выводит похожие посты
	"""
	user = None
	user_qs = User.objects.filter(username=context.get('user'))
	if user_qs.count() == 1:
		user = user_qs[0]
	recent_qs = Post.objects.for_user(user)[0:5]
	return {
		'recent_qs': Post.update_qs(recent_qs),
	}
