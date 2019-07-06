from ipaddress import ip_address

from django.shortcuts import render

from postapp.models import Post


def post_list(request):
    post_qs = Post.objects.all().order_by('-date_post')
    return render(
        request, 'postapp/post_list.html',
        {
        'post_list': post_qs
        }
    )


def post_detail(request, pk=None):
    if pk:
        post = Post.objects.get(pk=pk)
    else:
        post = Post.objects.all().order_by('-date_post')[0]
    return render(
        request, 'postapp/post_detail.html',
        {
        'post': post
        }
    )
