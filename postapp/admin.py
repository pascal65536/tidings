from django.contrib import admin
from postapp.models import Post, Charter


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'lead', 'date_post', 'deleted', )
    list_filter = ('charter', 'tags', )
    fieldsets = (
        (None, {
            'fields': ('title', 'lead', 'text', )
        }),
        ('Фильтрация', {
            'fields': ('charter', 'tags', )
        }),
        ('Изображения', {
            'fields': ('photo', )
        }),
        ('Даты', {
            'fields': ('date_post', 'deleted', )
        }),
        ('SEO', {
            'fields': ('og_picture', 'meta_title', 'meta_keywords', 'meta_description', )
        }),
    )


@admin.register(Charter)
class CharterAdmin(admin.ModelAdmin):
    list_display = ('title', 'lead', 'order')
    fieldsets = (
        (None, {
            'fields': ('title', 'lead', 'text')
        }),
        ('Фильтрация', {
            'fields': ('order',)
        }),
        ('Изображения', {
            'fields': ('picture', )
        }),
        ('SEO', {
            'fields': ('og_picture', 'meta_title', 'meta_keywords', 'meta_description')
        }),
    )
