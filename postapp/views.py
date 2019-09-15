import datetime
from django.utils.timezone import localtime, now

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from postapp.form import SearchForm
from postapp.models import Post, Charter, Site
from taggit.models import Tag


def post_index(request):
    post_queryset = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).order_by('-date_post')[0:3]
    charter = Charter.objects.filter(order__gt=0).order_by('order')
    meta_title = Site.objects.get(name='sitename')
    name_read_more = Site.objects.get(name='name_read_more').value

    return render(
        request, 'postapp/post_index.html',
        {
            'post_queryset': post_queryset,  # Все выводимые записи
            'charter': charter,  # Пункты меню
            'meta_title': meta_title,
            'name_read_more': name_read_more,
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
    name_recent_post = Site.objects.get(name='name_recent_post').value
    name_read_more = Site.objects.get(name='name_read_more').value
    sitename = Site.objects.get(name='sitename')

    post_queryset = post_queryset.order_by('-date_post')[0:len_recent_post]
    post_idx = set(post_queryset.values_list('id', flat=True))
    recent_post = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).exclude(id__in=post_idx).order_by('-date_post')[0:len_recent_post]
    charter = Charter.objects.filter(order__gt=0).order_by('order')
    post = None
    if len(post_queryset) > 0:
        post = post_queryset[0]

    meta_title = '%s | %s' % (post.charter.title, sitename)

    return render(
        request, 'postapp/post_list.html',
        {
            'post_queryset': post_queryset,  # Все выводимые записи
            'post': post,  # Единственная запись, по которой определим рубрику
            'recent_post': recent_post,  # Колонка записей
            'charter': charter,  # Пункты меню
            'meta_title': meta_title,
            'name_recent_post': name_recent_post,
            'name_read_more': name_read_more,
        }
    )


def post_detail(request, pk=None):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404

    len_recent_post = int(Site.objects.get(name='len_recent_post').value)
    name_recent_post = Site.objects.get(name='name_recent_post').value
    name_read_more = Site.objects.get(name='name_read_more').value
    sitename = Site.objects.get(name='sitename')
    recent_post = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).exclude(id=post.id).order_by('-date_post')[0:len_recent_post]
    charter = Charter.objects.filter(order__gt=0).order_by('order')

    meta_title = '%s | %s | %s' % (post.title, post.charter.title, sitename)

    return render(
        request, 'postapp/post_detail.html',
        {
            'post': post,  # Единственная запись
            'recent_post': recent_post,  # Колонка записей
            'charter': charter,  # Пункты меню
            'meta_title': meta_title,
            'name_recent_post': name_recent_post,
            'name_read_more': name_read_more,
        }
    )


def post_filter(request):
    post_queryset = Post.objects.filter(deleted__isnull=True, date_post__lte=datetime.datetime.now()).order_by('-date_post')
    charter = Charter.objects.filter(order__gt=0).order_by('order')
    name_read_more = Site.objects.get(name='name_read_more').value
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

    return render(
        request, 'postapp/post_filter.html',
        {
            'post_queryset': post_queryset,  # Все выводимые записи
            'charter': charter,
            'head_name': head_name,
            'meta_title': meta_title,
            'name_read_more': name_read_more,
        }
    )


"""
class TaggableManager([verbose_name="Tags", help_text="A comma-separated list of tags.", through=None, blank=False])
Parameters:	
    verbose_name – The verbose_name for this field.
    help_text – The help_text to be used in forms (including the admin).
    through – The through model, see Customizing taggit for more information.
    blank – Controls whether this field is required.

add(*tags)
This adds tags to an object. The tags can be either Tag instances, or strings:

apple.tags.all()
[]

apple.tags.add("red", "green", "fruit")

remove(*tags)
Removes a tag from an object. No exception is raised if the object doesn’t have that tag.

clear()
Removes all tags from an object.

set(*tags, clear=False)
If clear = True removes all the current tags and then adds the specified tags to the object. Otherwise sets the object’s tags to those specified, removing only the missing tags and adding only the new tags.

similar_objects()
Returns a list (not a lazy QuerySet) of other objects tagged similarly to this one, ordered with most similar first. Each object in the list is decorated with a similar_tags attribute, the number of tags it shares with this object.
If the model is using generic tagging (the default), this method searches tagged objects from all classes. If you are querying on a model with its own tagging through table, only other instances of the same model will be returned.

names()
Convenience method, returning a ValuesListQuerySet (basically just an iterable) containing the name of each tag as a string:

apple.tags.names()
[u'green and juicy', u'red']

slugs()
Convenience method, returning a ValuesListQuerySet (basically just an iterable) containing the slug of each tag as a string:

apple.tags.slugs()
[u'green-and-juicy', u'red']
"""