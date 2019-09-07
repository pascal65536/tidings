from django.contrib import admin

from postapp.models import Post, Charter, News, Content, Person


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Charter, PostAdmin)
# admin.site.register(News, PostAdmin)
# admin.site.register(Content, PostAdmin)
# admin.site.register(Person, PostAdmin)
