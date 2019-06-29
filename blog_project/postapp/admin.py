from django.contrib import admin

from postapp.models import Post


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post)
