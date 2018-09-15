"""newsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import contactapp.views as contactapp
import authorapp.views as authorapp


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^contact/', contactapp.contact, name='contact'),
    url(r'^author/', authorapp.author, name='author'),

#    url(r'^$', mainapp.main, name='main'),
#    url(r'^products/', mainapp.products, name='products'),

#    url(r'^item/([0-9]{1,})/', mainapp.item, name='item'),

    #url(r'^author/', include('authorapp.urls', namespace='author')),
    #url(r'^category/', include('categoryapp.urls', namespace='category')),
    #url(r'^news/', include('newsapp.urls', namespace='news')),
    #url(r'^pages/', include('contactapp.urls', namespace='pages')),

    #url(r'^$', RedirectView.as_view(url='/newsapp/', permanent=True)),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

