from django.contrib import admin
from authorapp.models import Author


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author)
