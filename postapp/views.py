import datetime
import re

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import TemplateView
from postapp.form import SearchForm, PostForm
from postapp.models import Post, Charter, Site
from taggit.models import Tag
from django.conf import settings


def get_seo(type=None, post=None):
    """
    SEO штуки и настройки для каждой страницы
    :param type: Тип страницы
    :param post: instance поста
    :return: Словарь с настройками
    """
    seo_dict = {
        'sitename': Site.objects.get(name='sitename'),
        'meta_title': Site.objects.get(name='sitename'),
        'keywords': Site.objects.get(name='keywords').value,
        'description': Site.objects.get(name='description').value,
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
    if type == 'index':
        return seo_dict

    if type == 'list':
        if post:
            sitename = Site.objects.get(name='sitename')
            seo_dict['meta_title'] = post.charter.meta_title or '%s | %s' % (post.charter.title, sitename)
            seo_dict['keywords'] = post.charter.meta_keywords or post.meta_keywords or ', '.join(post.tags.names())
            seo_dict['description'] = post.charter.meta_description or post.meta_description or post.lead
        return seo_dict

    if type == 'detail':
        sitename = Site.objects.get(name='sitename')
        meta_title = '%s | %s | %s' % (post.title, post.charter.title, sitename)
        if post.meta_title:
            meta_title = post.meta_title
        seo_dict['meta_title'] = meta_title

        keywords = ', '.join(post.tags.names())
        if post.meta_keywords:
            keywords = post.meta_keywords
        seo_dict['keywords'] = keywords

        description = post.lead
        if post.meta_description:
            description = post.meta_description
        seo_dict['description'] = description

        return seo_dict

    if type == 'filter':
        seo_dict['keywords'] = ', '.join(post.tags.names())
        seo_dict['description'] = post.meta_description or post.lead
        seo_dict['meta_title'] = post.meta_title or post.title

    return seo_dict


def post_index(request):
    main_post_queryset = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).order_by('-date_post')[0:4]
    main_post_idx = set(main_post_queryset.values_list('id', flat=True))
    post_queryset = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).exclude(id__in=main_post_idx).order_by('-date_post')[0:12]
    post_idx = set(post_queryset.values_list('id', flat=True))
    recent_post = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).exclude(id__in=post_idx).exclude(id__in=main_post_idx).order_by('-date_post')[0:6]
    charter = Charter.objects.filter(order__gt=0).order_by('order')

    return render(
        request, 'postapp/post_index.html',
        {
            'main_post_queryset': main_post_queryset,
            'post_queryset': post_queryset,  # Все выводимые записи
            'recent_post': recent_post,
            'charter': charter,  # Пункты меню
            'setting': get_seo(type='index'),  # SEO штуки и настройки для сайта
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
    post_idx = set(post_queryset.values_list('id', flat=True))
    recent_post = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).exclude(id__in=post_idx).order_by('-date_post')[0:len_recent_post]
    charter = Charter.objects.filter(order__gt=0).order_by('order')
    post = None
    if len(post_queryset) > 0:
        post = post_queryset[0]

    # Для opengrapf
    sitename = Site.objects.get(name='sitename')
    meta_title = '%s | %s' % (post.charter.title, sitename)
    og = {
        'title': meta_title,
        'description': post.charter.lead,
        'image': post.charter.og_picture,
        'type': 'website',
    }

    return render(
        request, 'postapp/post_list.html',
        {
            'post_queryset': post_queryset,  # Все выводимые записи
            'post': post,  # Единственная запись, по которой определим рубрику
            'recent_post': recent_post,  # Колонка записей
            'charter': charter,  # Пункты меню
            'og': og,  # Open Graph
            'setting': get_seo(type='list', post=post),  # SEO штуки и настройки для сайта
        }
    )


def post_detail(request, pk=None):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404

    len_recent_post = int(Site.objects.get(name='len_recent_post').value)
    recent_post = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).exclude(id=post.id).order_by('-date_post')[0:len_recent_post]
    charter = Charter.objects.filter(order__gt=0).order_by('order')

    # Для opengrapf
    sitename = Site.objects.get(name='sitename')
    meta_title = '%s | %s | %s' % (post.title, post.charter.title, sitename)
    if post.meta_title:
        meta_title = post.meta_title
    og = {
        'title': meta_title,
        'description': post.lead,
        'image': post.og_picture,
        'type': 'website',
    }

    return render(
        request, 'postapp/post_detail.html',
        {
            'post': post,  # Единственная запись
            'recent_post': recent_post,  # Колонка записей
            'charter': charter,  # Пункты меню
            'og': og,  # Open Graph
            'setting': get_seo(type='detail', post=post),  # SEO штуки и настройки для сайта
        }
    )


def post_filter(request):
    post_queryset = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).order_by('-date_post')
    charter = Charter.objects.filter(order__gt=0).order_by('order')

    sitename = Site.objects.get(name='sitename')
    head_name = None
    meta_title = None
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

    setting = get_seo(type='filter', post=post_queryset[0])  # SEO штуки и настройки для сайта
    if meta_title:
        setting['meta_title'] = meta_title

    return render(
        request, 'postapp/post_filter.html',
        {
            'post_queryset': post_queryset,  # Все выводимые записи
            'charter': charter,
            'head_name': head_name,
            'setting': setting,
        }
    )


@login_required
def post_edit(request, pk=None):

    form = PostForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        if request.FILES:
            cd.update({'picture': request.FILES.get('picture', None)})
        else:
            cd['picture'] = Post.objects.get(id=pk).picture

        try:
            post, _ = Post.objects.update_or_create(id=pk, defaults=cd)
            form = PostForm(instance=post)
        except Post.MultipleObjectsReturned:
            raise Http404

    else:
        try:
            form = PostForm(instance=Post.objects.get(pk=pk))
        except Post.DoesNotExist:
            raise Http404

    return render(
        request, 'postapp/post_edit.html',
        {
            'form': form.as_table(),
            'pk': pk,
        }
    )


def robots(request):
    return render(request, 'robots.txt', content_type="text/plain")


def delete_tags(value):
    value = re.sub(r'(\<(/?[^>]+)>)', '', value)
    value = re.sub(r'&[a-z]*;', ' ', value)
    return value


class YandexRss(TemplateView):
    template_name = 'rss/yandex.xml'
    filter = {
        'deleted': None
    }

    def get_context_data(self, **kwargs):
        ctx = super(YandexRss, self).get_context_data(**kwargs)
        post_qs = Post.objects.filter(date_post__lte=datetime.datetime.now()).order_by('-date_post')[0:25]
        for post in post_qs:
            post.title = delete_tags(post.title)
            post.lead = '<![CDATA[{}]]>'.format(delete_tags(post.lead))
            post.text = '<![CDATA[{}]]>'.format(delete_tags(post.text))
        ctx['object_list'] = post_qs
        ctx['static'] = settings.STATIC_URL
        ctx['media'] = settings.MEDIA_URL
        ctx['host'] = Site.objects.get(name='host')
        ctx['sitename'] = Site.objects.get(name='sitename')
        ctx['description'] = Site.objects.get(name='description')
        return ctx

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'text/xml; charset=UTF-8'
        return super(YandexRss, self).render_to_response(context, **response_kwargs)


class YandexDzenRss(TemplateView):
    template_name = 'rss/zen.xml'
    filter = {
        'deleted': None,
    }

    def get_context_data(self, **kwargs):
        ctx = super(YandexDzenRss, self).get_context_data(**kwargs)
        post_qs = Post.objects.filter(date_post__lte=datetime.datetime.now()).order_by('-date_post')[0:25]
        for post in post_qs:
            post.title = delete_tags(post.title)
            post.lead = '<![CDATA[{}]]>'.format(delete_tags(post.lead))
            post.text = '<![CDATA[{}]]>'.format(delete_tags(post.text))
            print (post.text)
        ctx['object_list'] = post_qs
        ctx['static'] = settings.STATIC_URL
        ctx['media'] = settings.MEDIA_URL
        ctx['host'] = Site.objects.get(name='host')
        ctx['sitename'] = Site.objects.get(name='sitename')
        ctx['description'] = Site.objects.get(name='description')
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
