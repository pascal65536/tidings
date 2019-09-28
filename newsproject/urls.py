from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from postapp.models import PostSitemap, PostFeed
from postapp.views import post_index, post_detail, post_list, post_filter, robots
from postapp.views import YandexDzenRss, YandexRss, YandexTurboRss


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_index, name='post_index'),
    url(r'^list/(?P<slug>\w+)/$', post_list, name='post_list'),
    url(r'^detail/(?P<pk>\d+)/$', post_detail, name='post_detail'),
    url(r'^filter/$', post_filter, name='post_filter'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'blog': PostSitemap}}),
    url(r'^feed/$', PostFeed()),
    url(r'^feed/yandex/$', YandexRss.as_view(), name='rss'),
    url(r'^feed/zen/$', YandexDzenRss.as_view(), name='zen'),
    url(r'^feed/turbo/$', YandexTurboRss.as_view(), name='turbo'),
    url(r'^robots\.txt$', robots),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
