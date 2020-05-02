from django import template
from django.utils import timezone
from postapp.models import Post

register = template.Library()


@register.simple_tag
def get_tags():
    tag_typle = Post.objects.filter(
        deleted__isnull=True, date_post__lte=timezone.now()).values_list(
        'tags__name', 'tags__slug')
    tag_dct = dict()
    for tag in tag_typle:
        if tag[1] and '0' not in tag[1]:
            tag_dct.setdefault(tag[1], {'name': tag[0], 'count': 0})
            tag_dct[tag[1]]['count'] += 1
    return tag_dct


@register.simple_tag
def get_calendar():
    post_qs = Post.objects.filter(deleted__isnull=True, date_post__lte=timezone.now())

    date_dct = dict()
    # date_format = "%d-%B-%Y"
    date_format = "%B %Y"
    date_format_slug = "%Y-%m"
    for post in post_qs:
        date_post = post.date_post.strftime(date_format)
        date_post_slug = post.date_post.strftime(date_format_slug)
        date_dct.setdefault(date_post_slug, {'name': date_post, 'count': 0})
        date_dct[date_post_slug]['count'] += 1
    return date_dct


