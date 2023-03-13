from django.contrib import admin
from .models import *

# Admin for UserAccount Model
class UserAccountAdmin(admin.ModelAdmin):
    list_display=(
        'user', 'profile_image', 'dob', 'bio'
    )
# Admin for Post Model
class PostAdmin(admin.ModelAdmin):
    list_display=(
        'post_id','user', 'post_date', 'caption', 'likes', 'image'
    )
# Admins for Friends Model
class FriendsAdmin(admin.ModelAdmin):
    list_display=('friend_a', 'friend_b', 'chat')
# Admin for FriendRequest Model
class FriendRequestAdmin(admin.ModelAdmin):
    list_display=('sender', 'receiver', 'status')
# Admin for Message Model
class MessageAdmin(admin.ModelAdmin):
    list_display=('chat', 'sender', 'date_sent', 'message')

# Register Admins for various Models
admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Friends, FriendsAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Message, MessageAdmin)