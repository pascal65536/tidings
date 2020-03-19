from django.contrib import admin
from postapp.models import Post, Charter, Site


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_post', 'deleted')
    list_filter = ('charter', 'tags')
    fieldsets = (
        (None, {
            'fields': ('title', 'lead', 'text')
        }),
        ('Фильтрация', {
            'fields': ('charter', 'tags')
        }),
        ('Изображения', {
            'fields': ('picture', )
        }),
        ('Даты', {
            'fields': ('date_post', 'deleted')
        }),
        ('SEO', {
            'fields': ('og_picture', 'meta_title', 'meta_keywords', 'meta_description')
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


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', )
