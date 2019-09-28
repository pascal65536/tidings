import datetime

from django.http import Http404
from django.shortcuts import render, get_object_or_404, render_to_response
from django.db.models import Q
from django.views.generic import TemplateView

from postapp.form import SearchForm
from postapp.models import Post, Charter, Site
from taggit.models import Tag


def post_index(request):
    post_queryset = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).order_by('-date_post')[0:3]
    charter = Charter.objects.filter(order__gt=0).order_by('order')
    meta_title = Site.objects.get(name='sitename')

    setting = {
        'meta_title': meta_title,
        'name_recent_post': Site.objects.get(name='name_recent_post').value,
        'name_read_more': Site.objects.get(name='name_read_more').value,
        'footer_text': Site.objects.get(name='footer_text').value,
        'footer_icons': Site.objects.get(name='footer_icons').value,
        'footer_contacts': Site.objects.get(name='footer_contacts').value,
        'footer_center': Site.objects.get(name='footer_center').value,
        'footer_head': Site.objects.get(name='footer_head').value,
        'footer_right': Site.objects.get(name='footer_right').value,
        'footer_counter': Site.objects.get(name='footer_counter').value,
    }

    return render(
        request, 'postapp/post_index.html',
        {
            'post_queryset': post_queryset,  # Все выводимые записи
            'charter': charter,  # Пункты меню
            'setting': setting,
        }
    )


def post_list(request, slug=None):
    post_queryset = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now())
    try:
        charter_slug = Charter.objects.get(slug=slug)
        post_queryset = post_queryset.filter(charter=charter_slug)
    except Charter.DoesNotExist:
        raise Http404

    len_recent_post = int(Site.objects.get(name='len_recent_post').value)
    sitename = Site.objects.get(name='sitename')

    post_queryset = post_queryset.order_by('-date_post')[0:len_recent_post]
    post_idx = set(post_queryset.values_list('id', flat=True))
    recent_post = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).exclude(id__in=post_idx).order_by('-date_post')[0:len_recent_post]
    charter = Charter.objects.filter(order__gt=0).order_by('order')
    post = None
    if len(post_queryset) > 0:
        post = post_queryset[0]

    meta_title = '%s | %s' % (post.charter.title, sitename)

    og = {
        'title': meta_title,
        'description': post.charter.lead,
        'image': post.charter.og_picture,
        'type': 'website',
    }

    setting = {
        'meta_title': meta_title,
        'name_recent_post': Site.objects.get(name='name_recent_post').value,
        'name_read_more': Site.objects.get(name='name_read_more').value,
        'footer_text': Site.objects.get(name='footer_text').value,
        'footer_icons': Site.objects.get(name='footer_icons').value,
        'footer_contacts': Site.objects.get(name='footer_contacts').value,
        'footer_center': Site.objects.get(name='footer_center').value,
        'footer_head': Site.objects.get(name='footer_head').value,
        'footer_right': Site.objects.get(name='footer_right').value,
        'footer_counter': Site.objects.get(name='footer_counter').value,
    }

    return render(
        request, 'postapp/post_list.html',
        {
            'post_queryset': post_queryset,  # Все выводимые записи
            'post': post,  # Единственная запись, по которой определим рубрику
            'recent_post': recent_post,  # Колонка записей
            'charter': charter,  # Пункты меню
            'og': og,  # Open Graph
            'setting': setting,
        }
    )


def post_detail(request, pk=None):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404

    len_recent_post = int(Site.objects.get(name='len_recent_post').value)
    sitename = Site.objects.get(name='sitename')
    recent_post = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).exclude(id=post.id).order_by('-date_post')[0:len_recent_post]
    charter = Charter.objects.filter(order__gt=0).order_by('order')

    meta_title = '%s | %s | %s' % (post.title, post.charter.title, sitename)

    og = {
        'title': meta_title,
        'description': post.lead,
        'image': post.og_picture,
        'type': 'website',
    }

    setting = {
        'meta_title': meta_title,
        'name_recent_post': Site.objects.get(name='name_recent_post').value,
        'name_read_more': Site.objects.get(name='name_read_more').value,
        'footer_text': Site.objects.get(name='footer_text').value,
        'footer_icons': Site.objects.get(name='footer_icons').value,
        'footer_contacts': Site.objects.get(name='footer_contacts').value,
        'footer_center': Site.objects.get(name='footer_center').value,
        'footer_head': Site.objects.get(name='footer_head').value,
        'footer_right': Site.objects.get(name='footer_right').value,
        'footer_counter': Site.objects.get(name='footer_counter').value,
    }

    return render(
        request, 'postapp/post_detail.html',
        {
            'post': post,  # Единственная запись
            'recent_post': recent_post,  # Колонка записей
            'charter': charter,  # Пункты меню
            'og': og,  # Open Graph
            'setting': setting,
        }
    )


def post_filter(request):
    post_queryset = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).order_by('-date_post')
    charter = Charter.objects.filter(order__gt=0).order_by('order')
    sitename = Site.objects.get(name='sitename')
    meta_title = sitename

    head_name = None
    form = SearchForm(data=request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data
        search_string = cd.get('search')
        post_queryset = post_queryset.filter(
            Q(title__icontains=search_string) | Q(lead__icontains=search_string) | Q(text__icontains=search_string))
        head_name = 'Все материалы по поиску «%s»:' % search_string
        meta_title = 'Все материалы по поиску «%s» | %s' % (search_string, sitename)

    slug_tag = request.GET.get('tag', None)
    if slug_tag:
        tag = get_object_or_404(Tag, slug=slug_tag)
        post_queryset = post_queryset.filter(tags__in=[tag])
        head_name = 'Все материалы по тегу «%s»:' % tag.name
        meta_title = 'Все материалы по тегу «%s» | %s' % (tag.name, sitename)

    setting = {
        'meta_title': meta_title,
        'name_recent_post': Site.objects.get(name='name_recent_post').value,
        'name_read_more': Site.objects.get(name='name_read_more').value,
        'footer_text': Site.objects.get(name='footer_text').value,
        'footer_icons': Site.objects.get(name='footer_icons').value,
        'footer_contacts': Site.objects.get(name='footer_contacts').value,
        'footer_center': Site.objects.get(name='footer_center').value,
        'footer_head': Site.objects.get(name='footer_head').value,
        'footer_right': Site.objects.get(name='footer_right').value,
        'footer_counter': Site.objects.get(name='footer_counter').value,
    }

    return render(
        request, 'postapp/post_filter.html',
        {
            'post_queryset': post_queryset,  # Все выводимые записи
            'charter': charter,
            'head_name': head_name,
            'setting': setting,
        }
    )


def robots(request):
    return render_to_response('robots.txt', content_type="text/plain")


class YandexRss(TemplateView):
    template_name = 'rss/yandex.xml'
    filter = {'deleted': None}

    def get_context_data(self, **kwargs):
        ctx = super(YandexRss, self).get_context_data(**kwargs)
        # qs = Post.objects.filter(**self.filter).order_by('-date_post')
        qs = Post.objects.filter(date_post__lte=datetime.datetime.now()).order_by('-date_post')[0:25]
        ctx['object_list'] = qs
        ctx['host'] = Site.objects.get(name='host')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'text/xml; charset=UTF-8'
        return super(YandexRss, self).render_to_response(context, **response_kwargs)


class YandexDzenRss(TemplateView):
    template_name = 'rss/zen.xml'
    filter = {
        'deleted': None,
        'charter': 1,
    }

    def get_context_data(self, **kwargs):
        ctx = super(YandexDzenRss, self).get_context_data(**kwargs)
        qs = Post.objects.filter(**self.filter).order_by('-date_post')
        # qs = Post.objects.filter(date_post__lte=datetime.datetime.now()).order_by('-date_post')[0:25]
        ctx['object_list'] = qs
        ctx['host'] = Site.objects.get(name='host')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'text/xml; charset=UTF-8'
        return super(YandexDzenRss, self).render_to_response(context, **response_kwargs)


class YandexTurboRss(TemplateView):
    template_name = 'rss/turbo.xml'
    filter = {
        'deleted': None,
        'charter': 1,
    }

    def get_context_data(self, **kwargs):
        ctx = super(YandexTurboRss, self).get_context_data(**kwargs)
        ctx['object_list'] = Post.objects.filter(**self.filter).order_by('-date_post')
        ctx['host'] = Site.objects.get(name='host')
        ctx['charter'] = Charter.objects.filter(order__gt=0).order_by('order')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'text/xml; charset=UTF-8'
        return super(YandexTurboRss, self).render_to_response(context, **response_kwargs)
