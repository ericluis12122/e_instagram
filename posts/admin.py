from django.contrib import admin

from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'caption')
    list_filter = ('user', 'created_at')
    search_fields = ('user', 'caption')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'content')
    list_filter = ('user', 'created_at')
    search_fields = ('user', 'content')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
