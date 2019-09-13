from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin

from postapp.views import post_index, post_detail, post_list


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_index, name='post_index'),
    url(r'^list/(?P<slug>\w+)/$', post_list, name='post_list'),
    url(r'^detail/(?P<pk>\d+)/$', post_detail, name='post_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

