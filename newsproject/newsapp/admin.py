from django.contrib import admin
from newsapp.models import News


class NewsAdmin(admin.ModelAdmin):
    pass

admin.site.register(News)



