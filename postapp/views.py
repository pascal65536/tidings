import requests
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.template import loader, Context

from newsapp.views import news_detail
from newsproject.utils import get_tags, cyr_lat
from photoapp.models import Photo
from postapp.form import PostForm, CharterForm, TagForm
from postapp.models import Post, Charter
from taggit.models import Tag
from django.conf import settings


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
        'seo': settings.SEO,
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
        'seo': settings.SEO,
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
    return redirect(news_detail, post.pk)


@login_required(login_url='/login/')
@staff_member_required
def charter_view(request):
    """
    Галерея категорий
    """
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
        'seo': settings.SEO,
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
        'seo': settings.SEO,
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
        'seo': settings.SEO,
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
        'seo': settings.SEO,
    })
