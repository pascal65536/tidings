from django import template
from postapp.models import Post
from django.utils import timezone
from django.core.cache import cache

register = template.Library()


@register.simple_tag
def get_tags():
    tag_typle = Post.objects.filter(
        deleted__isnull=True, date_post__lte=timezone.now()).values_list(
        'tags__name', 'tags__slug')
    tag_dct = cache.get('tag', {})
    for tag in tag_typle:
        if tag[1] and '0' not in tag[1]:
            dct = tag_dct.setdefault(tag[1], {'name': tag[0], 'count': 0})
            dct['count'] += 1
        cache.set(f'weather', tag_dct, 2 * 60 * 60)
        cache.set(f'weather_lte', tag_dct, 12 * 60 * 60)
    return tag_dct
