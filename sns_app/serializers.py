from rest_framework import serializers
from .models import *

# Serializer for UserAccount Model
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['profile_image', 'dob', 'bio']

# Serializer for Post Model
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_id', 'user', 'post_date', 'caption', 
                    'likes', 'image']

# Serializer combining User, UserAccount and Post Models
class UserSerializer(serializers.ModelSerializer):
    profile = UserAccountSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','profile','posts']

# Serializer for Friend Model
class FriendsSerializer(serializers.ModelSerializer):
    friend_a = UserSerializer
    friend_b = UserSerializer

    class Meta:
        model=Friends
        fields=['friend_a', 'friend_b', 'chat']

# Serializer for Friend Request Model
class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer
    receiver = UserSerializer

    class Meta:
        model=FriendRequest
        fields=['sender', 'receiver', 'status']

# Serializer for Messages Model
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer

    class Meta:
        model=Message
        fields=['chat', 'sender', 'date_sent', 'message']