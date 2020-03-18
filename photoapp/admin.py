from django.contrib import admin
from photoapp.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_img', 'picture', )
    list_filter = ('changed', )
    fieldsets = (
        (None, {'fields': ('title', 'picture',)}),
    )
