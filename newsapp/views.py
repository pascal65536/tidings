from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from taggit.models import Tag

from newsproject import settings
from newsproject.defaults import SEO
from newsproject.utils import get_recent_for_tags, process_text
from postapp.models import Charter, Post


def news_view(request):
    """
    Галерея новостей
    """
    message = None
    filter_dct = dict()
    slug_tag = request.GET.get('tag')

    post_qs = Post.objects.for_user(request.user)
    if slug_tag:
        filter_dct.update(
            {'tags__slug': slug_tag}
        )
        tag_obj = get_object_or_404(Tag, slug=slug_tag)
        message = f'Все посты по тегу "{tag_obj}"'

    slug = request.GET.get('charter')
    if slug:
        charter = get_object_or_404(Charter, slug=slug)
        filter_dct.update(
            {'charter': charter}
        )
        message = f'Все посты в категории "{charter.title}"'

    date = request.GET.get('date')
    if date:
        filter_dct.update(
            {'date_post__startswith': date}
        )
        message = f'Все материалы за дату "{date}"'

    query = request.GET.get('query')
    if query:
        query = query.strip()
        post_qs = post_qs.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(lead__icontains=query)
        )
        message = f'Все посты по поиску "{query}"'

    filter_dct.update(
        {'deleted__isnull': True,
         'date_post__lte': timezone.now()},
    )

    post_qs = post_qs.filter(**filter_dct)
    main_qs = post_qs.order_by('-date_post')[0:6]
    main_idx = set(main_qs.values_list('id', flat=True))
    recent_qs = post_qs.exclude(id__in=main_idx).order_by('-date_post')
    return render(request, "newsapp/news_view.html", {
        'main_qs': Post.update_qs(main_qs),
        'recent_qs': recent_qs,
        'message': message,
        'seo': SEO,
    })


def news_detail(request, pk=None):
    """
    Детали поста
    """
    post_qs = Post.objects.for_user(request.user)
    try:
        instance_qs = post_qs.filter(pk=pk)
        if len(instance_qs) != 1:
            raise Http404
        instance = instance_qs[0]
    except Charter.DoesNotExist:
        raise Http404
    instance.text = process_text(instance.text)
    recent_post_idx = get_recent_for_tags(instance, request.user)
    recent_post_qs = Post.objects.filter(id__in=recent_post_idx[0:12])

    return render(request, "newsapp/news_detail.html", {
        'instance': instance,
        'active': instance.charter.slug,
        'recent_post_qs': recent_post_qs,
    })
