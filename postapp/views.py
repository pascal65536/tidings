import requests
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.template import loader, Context

from newsproject.utils import get_tags, cyr_lat
from photoapp.models import Photo
from postapp.form import SearchForm, PostForm, CharterForm, TagForm
from postapp.models import Post, Charter, Site
from taggit.models import Tag
from django.conf import settings
from django.utils import timezone


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


def get_recent_post(exclude_post_idx, post_id=None, user=None):
    len_recent_post = int(Site.objects.get(name='len_recent_post').value)
    recent_post = Post.objects.filter(
        deleted__isnull=True, date_post__lte=timezone.now())

    if post_id:
        recent_post = recent_post.exclude(
            id__in=[post_id]).order_by('-date_post')[0:len_recent_post]
        if user and user.is_staff:
            post_view = Post.objects.get(id=post_id)
            post_dct = dict()
            for tag in post_view.tags.all():
                post_idx = Post.objects.filter(tags__in=[tag]).values_list('id', flat=True)
                for pst in post_idx:
                    post_dct.setdefault(pst, 0)
                    post_dct[pst] += 1

            idx_lst = list()
            for k, v in post_dct.items():
                if not k == post_id and v in sorted(post_dct.values())[-3:]:
                    idx_lst.append(k)

            recent_post = Post.objects.filter(id__in=idx_lst)
            return recent_post

        return recent_post

    recent_post = recent_post.exclude(
        id__in=exclude_post_idx).order_by('-date_post')[0:len_recent_post]
    return recent_post


def post_index(request):
    main_post_queryset = Post.objects.filter(deleted__isnull=True, date_post__lte=timezone.now()).order_by('-date_post')[0:4]
    main_post_idx = set(main_post_queryset.values_list('id', flat=True))
    post_queryset = Post.objects.filter(deleted__isnull=True, date_post__lte=timezone.now()).exclude(id__in=main_post_idx).order_by('-date_post')[0:12]
    exclude_post_idx = set(post_queryset.values_list('id', flat=True)) | main_post_idx
    charter = Charter.objects.filter(order__gt=0).order_by('order')

    return render(
        request, 'postapp/post_index.html',
        {
            'main_post_queryset': Post.update_qs(main_post_queryset),
            'post_queryset': Post.update_qs(post_queryset),  # Все выводимые записи
            'recent_post': Post.update_qs(get_recent_post(exclude_post_idx)),
            'charter': charter,  # Пункты меню
            'setting': get_seo(type='index'),  # SEO штуки и настройки для сайта
        }
    )


def post_detail(request, pk=None):
    try:
        fields = {'pk': pk}
        if not request.user.is_staff:
            fields.update({'deleted__isnull': True, 'date_post__lte': timezone.now()})
        post = Post.objects.get(**fields)
    except Post.DoesNotExist:
        raise Http404

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
            'recent_post': Post.update_qs(get_recent_post(set(), post_id=post.id, user=request.user)),
            'charter': charter,  # Пункты меню
            'og': og,  # Open Graph
            'setting': get_seo(type='detail', post=post),  # SEO штуки и настройки для сайта
        }
    )


@login_required(login_url='/login/')
@staff_member_required
def post_edit(request, pk=None):
    """
    Редактирование поста
    """
    instance = None
    if pk:
        instance = get_object_or_404(Post, pk=pk)
        post_qs = Post.objects.filter(pk=instance.id)
        tags_lst = get_tags(post_qs)
        for tags in tags_lst:
            instance.tags.add(tags)
        instance = get_object_or_404(Post, pk=pk)

    images_list = [('', '---')]
    if instance:
        picture = None
        if instance.photo and instance.photo.picture and instance.photo.picture.name:
            picture = instance.photo.picture.name
        photo_obj = Photo.objects.filter(picture=picture)
        if photo_obj.count() == 1:
            images_list.append((photo_obj[0].id, photo_obj[0].title),)
        photo_qs = Photo.objects.all().exclude(picture=picture).order_by('-changed')[:10]
        for photo in photo_qs:
            images_list.append((photo.id, photo.title), )

    form = PostForm(data=request.POST or None, files=request.FILES or None, instance=instance, images_list=images_list)
    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        post = form.save(commit=False)
        post.picture = None
        post.save()
        # Нельзя добавить теги к несуществующему объекту.
        post.tags.clear()
        for tags in cd.get('tags'):
            post.tags.add(tags)

        return redirect(post_view)

    return render(request, "postapp/post_edit.html", {
        'form': form,
        'instance': instance,
        'active': 'post',
    })


@login_required(login_url='/login/')
@staff_member_required
def post_view(request):
    """
    Галерея постов
    """
    message = None
    filter_dct = dict()
    slug_tag = request.GET.get('tag')
    if slug_tag:
        filter_dct.update(
            {'tags__slug': slug_tag}
        )
        tag_obj = get_object_or_404(Tag, slug=slug_tag)
        message = f'Все посты по тегу "{tag_obj}"'

    slug = request.GET.get('charter')
    if slug:
        charter = Charter.objects.get(slug=slug)
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

    post_qs = Post.objects.filter(**filter_dct)
    query = request.GET.get('query')
    if query:
        query = query.strip()
        post_qs = post_qs.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(lead__icontains=query)
        )
        message = f'Все посты по поиску "{query}"'

    return render(request, "postapp/post_view.html", {
        'post_qs': post_qs.order_by('deleted', '-changed'),
        'active': 'post',
        'message': message,
    })


def robots(request):
    return render(request, 'robots.txt', content_type="text/plain")


@login_required(login_url='/login/')
@staff_member_required
def post_content(request, pk=None):
    """
    Проверка на плагиат
    """
    post = get_object_or_404(Post, pk=pk)
    text = post.text
    url = 'https://content-watch.ru/public/api/'

    data = {
        'action': 'CHECK_TEXT',
        'key': settings.API_KEY,
        'test': 0,
        'text': text
    }
    req = requests.post(url, data=data)
    req.encoding = 'utf-8'
    result_dct = req.json()
    post.title = f"{post.title}|{result_dct.get('percent')}"
    post.save()
    return redirect(post_detail, post.pk)


@login_required(login_url='/login/')
@staff_member_required
def charter_view(request):
    """
    Галерея категорий
    """
    user = None
    message = None
    filter_dct = dict()
    charter_qs = Charter.objects.filter(**filter_dct)

    query = request.GET.get('query')
    if query:
        query = query.strip()
        charter_qs = charter_qs.filter(
            Q(title__icontains=query) |
            Q(lead__icontains=query)
        )
        message = f'Все категории по поиску "{query}"'
    user = request.user
    charter_dct = dict(Post.objects.for_user(user).order_by().values_list('charter_id').annotate(count=Count('id')))
    for charter in charter_qs:
        charter.count = charter_dct.get(charter.id, None)

    return render(request, "postapp/charter_view.html", {
        'charter_qs': charter_qs,
        'active': 'charter',
        'message': message,
    })


@login_required(login_url='/login/')
@staff_member_required
def charter_edit(request, pk=None):
    instance = None
    if pk:
        instance = get_object_or_404(Charter, pk=pk)
    form = CharterForm(data=request.POST or None, files=request.FILES or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        charter = form.save(commit=False)
        charter.slug = cyr_lat(cd['title'])
        charter.save()
        return redirect(charter_view)

    return render(request, "postapp/charter_edit.html", {
        'form': form,
        'instance': instance,
        'active': 'charter',
    })


def error404(request):
    template = loader.get_template('404.htm')
    context = Context({
        'message': 'All: %s' % request,
        })
    return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404)


@login_required(login_url='/login/')
@staff_member_required
def tags_view(request):
    message = None
    tags_qs = Tag.objects.all()
    query = request.GET.get('query')
    if query:
        query = query.strip()
        tags_qs = tags_qs.filter(
            Q(name__icontains=query) |
            Q(slug__icontains=query)
        )
        message = f'Все теги по поиску "{query}"'

    return render(request, "postapp/tags_view.html", {
        'tags_qs': tags_qs.order_by('name'),
        'active': 'tags',
        'message': message,
    })


@login_required(login_url='/login/')
@staff_member_required
def tags_edit(request, pk=None):
    """
    Добавить или отредактировать тег
    """
    tag = None
    if pk:
        tag = get_object_or_404(Tag, pk=pk)
    form = TagForm(data=request.POST or None, files=request.FILES or None, instance=tag)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(tags_view)

    return render(request, "postapp/tags_edit.html", {
        'form': form,
        'tag': tag,
        'active': 'tags',
    })
