from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.sitemaps.views import sitemap

from photoapp.views import photo_view, photo_edit
from postapp.views import post_index, post_detail, post_list, post_filter, robots, post_edit, post_content, post_view, \
    charter_view, charter_edit, tags_view, tags_edit
from postapp.models import PostFeed, PostSitemap, YandexRss, YandexDzenRss, YandexTurboRss

from rssapp.views import show_content, news_detail
from django.conf import settings

urlpatterns = [
    url(r'login/$', views.LoginView.as_view(), name='login'),
    url(r'logout/$', views.LogoutView.as_view(next_page='/'), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_index, name='post_index'),
    url(r'^list/(?P<slug>\w+)/$', post_list, name='post_list'),
    url(r'^photo/$', photo_view, name='photo_view'),
    url(r'^photo/add/', photo_edit, name='photo_add'),
    url(r'^photo/(?P<pk>\d+)/edit/', photo_edit, name='photo_edit'),

    url(r'^post/$', post_view, name='post_view'),
    url(r'^post/add/', post_edit, name='post_add'),
    url(r'^post/(?P<pk>\d+)/edit/', post_edit, name='post_edit'),

    url(r'^charter/$', charter_view, name='charter_view'),
    url(r'^charter/add/', charter_edit, name='charter_add'),
    url(r'^charter/(?P<pk>\d+)/edit/', charter_edit, name='charter_edit'),

    url(r'tags/$', tags_view, name='tags_view'),
    url(r'tags/add/$', tags_edit, name='tags_add'),
    url(r'tags/(?P<pk>\d+)/edit/$', tags_edit, name='tags_edit'),

    url(r'^detail/(?P<pk>\d+)/$', post_detail, name='post_detail'),
    url(r'^content/(?P<pk>\d+)/$', post_content, name='post_content'),
    url(r'^filter/$', post_filter, name='post_filter'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'blog': PostSitemap}}),
    url(r'^feed/$', PostFeed()),
    url(r'^rss/yandex/$', YandexRss.as_view(), name='rss'),
    url(r'^rss/zen/$', YandexDzenRss.as_view(), name='zen'),
    url(r'^rss/turbo/$', YandexTurboRss.as_view(), name='turbo'),
    url(r'^robots\.txt$', robots),
    url(r'news/', show_content, name='show_content'),
    url(r'news_detail/(?P<pk>\d+)/$', news_detail, name='news_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path, include, re_path
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
