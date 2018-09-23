from django.conf.urls import url
import authorapp.views as authorapp


urlpatterns = [
    url(r'^$', authorapp.author, name='author'),
    url(r'(?P<nickname>\w+)', authorapp.person, name='person'),
]


