from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin

from authorapp.views import author, person
from contactapp.views import contact
from postapp.views import post_index, post_detail, post_list


urlpatterns = [
    url(r'^author', author, name='author'),
    url(r'^author/(?P<slug>[\w-]+)', person, name='person'),
    url(r'^admin/', admin.site.urls),
    url(r'^contact/', contact, name='contact'),
    url(r'^$', post_index, name='post_index'),
    url(r'^post_list/', post_list, name='post_list'),
    url(r'^post_detail/', post_detail, name='post_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

