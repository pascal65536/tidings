from django.contrib import admin
from pagesapp.models import Contacts


class ContactsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Contacts)

