from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from taggit.models import Tag

from newsproject.utils import get_tags
from photoapp.forms import PhotoForm
from photoapp.models import Photo
from postapp.models import Post


@login_required(login_url='/login/')
@staff_member_required
def photo_edit(request, pk=None):
    """
    Добавить или отредактировать фото
    """
    instance = None
    if pk:
        instance = get_object_or_404(Photo, pk=pk)
        post_qs = Post.objects.filter(photo_id=instance.id)
        tags_lst = get_tags(post_qs)
        for tags in tags_lst:
            instance.tags.add(tags)

    form = PhotoForm(data=request.POST or None, files=request.FILES or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(photo_view)

    return render(request, "photoapp/photo_edit.html", {
        'form': form,
        'instance': instance,
        'active': 'photo',
    })


@login_required(login_url='/login/')
@staff_member_required
def photo_view(request):
    """
    Фотогалерея
    :param request:
    :return:
    """
    message = None
    filter_dct = dict()
    slug_tag = request.GET.get('tag')
    if slug_tag:
        filter_dct.update(
            {'tags__slug': slug_tag}
        )
        tag_obj = get_object_or_404(Tag, slug=slug_tag)
        message = f'Все фотографии по тегу "{tag_obj}"'

    photo_qs = Photo.objects.filter(**filter_dct)
    query = request.GET.get('query')
    if query:
        query = query.strip()
        photo_qs = photo_qs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
        message = f'Все фотографии по поиску "{query}"'

    return render(request, "photoapp/photo_view.html", {
        'photo_qs': photo_qs.order_by('deleted', '-changed'),
        'active': 'photo',
        'message': message,
    })


from django.shortcuts import render
from django.template import RequestContext


def e_handler404(request):
    context = RequestContext(request)
    response = render('404.html', context)
    response.status_code = 404
    return response


def e_handler500(request):
    context = RequestContext(request)
    response = render('500.html', context)
    response.status_code = 500
    return response
