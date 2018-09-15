from django.contrib import admin
from pagesapp.models import Contacts


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')


admin.site.register(Contacts)

