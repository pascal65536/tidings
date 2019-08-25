from django.contrib import admin
from contactapp.models import Contact


class ContactAdmin(admin.ModelAdmin):
    pass


admin.site.register(Contact)
