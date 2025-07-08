from django.contrib import admin
from .models import News, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date')
    search_fields = ('title', 'content')
    list_filter = ('pub_date', 'author')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'created_at')
    search_fields = ('text',)
    list_filter = ('created_at',)
