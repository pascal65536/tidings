from django.conf.urls.static import static
from django.contrib import admin
from postapp import views as postapp_views
from django.conf.urls import url
from blog_project import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^post_list/', postapp_views.post_list, name='post_list'),
    url(r'^post_detail/', postapp_views.post_detail, name='post_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)