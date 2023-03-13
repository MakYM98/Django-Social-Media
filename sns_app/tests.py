# Create your tests here.
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import auth

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient


from .model_factories import *
from .serializers import *
from .forms import*

# Serializer Tests
class SerializerTest(APITestCase):
    def setUp(self):
        # Create User Factory object & Serializer    
        self.user = UserFactory.create()
        self.userSerializer = UserSerializer(instance=self.user)
        # Create User Account Factory Object & Serializer   
        self.userAcc = UserAccountFactory.create()
        self.userAccSerializer = UserAccountSerializer(instance=self.userAcc)
        # Create Post Factory Object & Serializer   
        self.post = PostFactory.create()
        self.postSerializer = PostSerializer(instance=self.post)
        # Create Friends Factory Object & Serializer   
        self.friends = FriendsFactory.create()
        self.friendsSerializer = FriendsSerializer(instance=self.friends)
        # Create Friends Request Factory Object & Serializer   
        self.friendReq = FriendRequestFactory.create()
        self.friendReqSerializer = FriendRequestSerializer(instance=
                                                           self.friendReq)
        # Create Friends Request Factory Object & Serializer   
        self.message = MessageFactory.create()
        self.messageSerializer = MessageSerializer(instance=self.message)

    # Test that User Serializer has correct keys
    def test_useracc_correct_fields(self):
        data = self.userAccSerializer.data
        self.assertEqual(set(data.keys()), set(['profile_image', 'dob', 'bio']))

    # Test that Post Serializer has correct keys
    def test_post_correct_fields(self):
        data = self.postSerializer.data
        self.assertEqual(set(data.keys()), set(['post_id', 'user', 'post_date', 
                                                'caption', 'likes', 'image']))
    
    # Test that Friend Serializer has correct keys
    def test_friends_correct_fields(self):
        data = self.friendsSerializer.data
        self.assertEqual(set(data.keys()), set(['friend_a', 'friend_b', 
                                                'chat']))
    
    # Test that Friend Request Serializer has correct keys
    def test_friendrequest_correct_fields(self):
        data = self.friendReqSerializer.data
        self.assertEqual(set(data.keys()), set(['sender', 'receiver', 
                                                'status']))

    # Test that Message Serializer has correct keys
    def test_message_correct_fields(self):
        data = self.messageSerializer.data
        self.assertEqual(set(data.keys()), set(['chat', 'sender', 'date_sent',
                                                'message']))

# Test Class for Views
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        # Store all reverse urls
        self.home_url = reverse('home')
        self.register_url = reverse('signup')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.edit_profile_url = reverse('edit_profile')
        self.user_profile_url = reverse('user_profile')
        self.create_post_url = reverse('create_post')
        self.friend_list_url = reverse('friend_list')
        self.friend_request_url = reverse('friend-request')
        self.other_users_url = reverse('other_users', args=['jrandomuser'])
        self.user_friends_url = reverse('user-friends', args=['jrandomuser'])
        self.user_search_url = reverse('search-user')
        self.chat_room_url = reverse('chat-room', args=['testroom'])
        self.chat_list_url = reverse('chat_list')
        self.save_message_url = reverse('save_message')
        self.unfriend_url = reverse('unfriend')
        # User 1 Details
        self.username = "jrandomuser"
        self.password = "qwerty123"
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        # User 2 Details
        self.username2 = "randomuser2"
        self.password2 = "abcdefg"
        self.user2 = User.objects.create(username=self.username2)
        self.user2.set_password(self.password)
        self.user2.save()
        # User 1 UserAccount Object
        self.user_account = UserAccount.objects.create(user=self.user)
        # User 1 Post Object
        self.post = Post.objects.create(user=self.user)
        # User 1 & 2 Friends Object
        self.friend = Friends.objects.create(
                                                friend_a=self.user, 
                                                friend_b=self.user2, 
                                                chat="test-chat"
                                            )
        # User 1 & Random User Friend Request
        self.friend_req = FriendRequestFactory.create(
                                                sender=self.user, 
                                                receiver=UserFactory.create(), 
                                                status='pending'
                                            )
        # Login to Client with User 1 Details
        self.client.login(username=self.username, password=self.password)

    # Check that Home View is using the correct HTML File
    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/home_base.html')
    # Check that Register View is using the correct HTML File
    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/signup.html')
    # Check that Login View is using the correct HTML File
    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/login.html')
    # Check that Logout View is using the correct HTML File
    def test_logout_view(self):
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)
    # Check that Edit Profile View is using the correct HTML File
    def test_edit_profile_view(self):
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/edit_profile.html')
    # Check that Profile View is using the correct HTML File
    def test_user_profile_view(self):
        response = self.client.get(self.user_profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/user_profile.html')
    # Check that Create Post View is using the correct HTML File
    def test_create_post_view(self):
        response = self.client.get(self.create_post_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/new_post.html')
    # Check that Friend List View is using the correct HTML File
    def test_friend_list_view(self):
        response = self.client.get(self.friend_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/friend_list.html')
    # Check that Friend Request View is using the correct HTML File
    def test_friend_request_view(self):
        response = self.client.get(self.friend_request_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/friend_request.html')
    # Check that Other User Profile View is using the correct HTML File
    def test_other_profile_view(self):
        response = self.client.get(self.other_users_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/other_user_profile.html')
    # Check that Other User Friend List View is using the correct HTML File
    def test_other_friend_list_view(self):
        response = self.client.get(self.user_friends_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/friend_list.html')
    # Check that Chat Room View is using the correct HTML File
    def test_chat_room_view(self):
        response = self.client.get(self.chat_room_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/chat_room.html')
    # Check that List of Chats View is using the correct HTML File
    def test_chat_list_view(self):
        response = self.client.get(self.chat_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'snsApp/chat_list.html')

# Test Class for User List API
class UserListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory.create()
        self.userSerializer = UserSerializer(instance=self.user)
    #  Test GET endpoint to ensure it returns the correct data.
    def test_get_user_list(self):
        response = self.client.get(reverse('user_list', args=
                                           [self.user.username]))
        users = User.objects.filter(username=self.user.username)
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test Class for Post List API
class PostsListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post = PostFactory.create()
        self.postSerializer = PostSerializer(instance=self.post)
    # Test GET endpoint to ensure it returns the correct data.
    def test_get_post_list(self):
        response = self.client.get(reverse('post', args=[self.post.post_id]))
        self.assertEqual(response.data[0], self.postSerializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Test Class for New Post API
class NewPostListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory.create()
    # Test POST endpoint successfully creates new post.
    def test_create_new_post(self):
        data = {
            'user': self.user.pk,
            'caption': 'New Post', 
            'likes': 1,
            'image': open('./sns_app/static/img/favicon.ico', 'rb'),
            'post_date': '2023-03-04'
        }
        response = self.client.post(reverse('new_post'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
