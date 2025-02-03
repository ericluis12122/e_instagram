from django.contrib import admin

from .models import UserProfile, Follow

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date']
    search_fields = ['user__username']
    list_filter = ['birth_date']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    search_fields = ['follower__user__username', 'following__user__username']
    list_filter = ['created_at']