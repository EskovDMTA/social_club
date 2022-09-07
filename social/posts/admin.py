from django.contrib import admin

# Register your models here.
from .models import Posts, Group, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'image')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = 'none'

admin.site.register(Posts, PostAdmin)
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Follow)