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
            dct = tag_dct.setdefault(tag[1], {'name': tag[0], 'count': 0})
            dct['count'] += 1
    return tag_dct
