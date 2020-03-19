from django.shortcuts import render, get_object_or_404
from rssapp.models import Content, BaseUrl, Article


def news_detail(request, pk=None):
    content_qs = Content.objects.filter(pk=pk)
    content_qs.update(is_read=True)
    return render(
        request, 'rssapp/news_detail.html',
        {
            'content': content_qs[0],
        }
    )


def show_content(request):
    bu_id = request.GET.get('bu', None)
    content_qs = Content.objects.exclude(pic=None)
    if bu_id:
        content_qs = content_qs.filter(baseurl__id=bu_id)
    content_qs = content_qs.order_by('-published')
    return render(
        request, 'rssapp/show_content.html',
        {
            'content_qs': content_qs,
        }
    )


def index(request):
    article_qs = Article.objects.all()
    return render(
        request, 'rssapp/index.html',
        {
            'article_qs': article_qs,
        }
    )