from django.contrib import admin

from postapp.models import Post, Charter, News, Content, Person


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'charter', 'date_post')
    list_filter = ('charter',)
    # fields = ['title', 'lead', 'text', 'charter', 'tags', 'picture', 'og_picture', ('date_post', 'deleted')]
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

# admin.site.register(Post, PostAdmin)
# admin.site.register(Charter, PostAdmin)
# admin.site.register(News, PostAdmin)
# admin.site.register(Content, PostAdmin)
# admin.site.register(Person, PostAdmin)
