from django.contrib import admin
from .models import Post, Comment, Follow, Notification

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'likes', 'caption']
    list_filter = ['user', 'likes', 'caption']


class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'date_followed']
    list_filter = ['follower', 'following', 'date_followed']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'notification_type']
    list_filter = ['from_user', 'to_user', 'notification_type']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'date_created']
    list_filter = ['user', 'post', 'date_created']


admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Comment, CommentAdmin)
