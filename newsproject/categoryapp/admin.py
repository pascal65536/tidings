from django.contrib import admin
from categoryapp.models import Content, Person


class CategoryAdmin(admin.ModelAdmin):
    pass


class ContentAdmin(admin.ModelAdmin):
    pass


class PersonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Content)
admin.site.register(Person)


