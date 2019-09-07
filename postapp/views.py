from django.shortcuts import render, get_object_or_404
from postapp.models import Post
from taggit.models import Tag


def post_index(request):
    print('-' * 80)
    post_qs = Post.objects.all().order_by('-date_post')[0:3]
    post = {
        'left': post_qs[0],
        'center': post_qs[1],
        'right': post_qs[2],
    }

    return render(
        request, 'postapp/post_index.html',
        {
            'post': post,
        }
    )


def post_list(request):
    post_queryset = Post.objects.all().order_by('-date_post')
    tag = None
    slug = request.GET.get('tag', None)
    if slug:
        tag = get_object_or_404(Tag, slug=slug)
        post_queryset = Post.objects.filter(tags__in=[tag]).order_by('-date_post')
    # Все индексы постов, попавших в этот тег
    post_idx = set(post_queryset.values_list('id', flat=True))
    len_recent_post = 6
    recent_post = Post.objects.all().exclude(id__in=post_idx).order_by('-date_post')[0:len_recent_post]

    return render(
        request, 'postapp/post_list.html',
        {
            'post_queryset': post_queryset,
            'recent_post': recent_post,
            'tag': tag,
        }
    )


def post_detail(request):
    if request.GET.get('post', None):
        post = Post.objects.get(id=request.GET.get('post', None))
    else:
        post = Post.objects.all().order_by('-date_post')[0]

    len_recent_post = 6
    recent_post = Post.objects.all().exclude(id=post.id).order_by('-date_post')[0:len_recent_post]

    return render(
        request, 'postapp/post_detail.html',
        {
            'post': post,
            'recent_post': recent_post,
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