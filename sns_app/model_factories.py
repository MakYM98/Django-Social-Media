import factory
from django.contrib.auth.models import User
from django.test import TestCase
from .models import *
import uuid

# Factory for User Model
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('user_name', locale='en_GB')
    email = factory.Faker('email')
    password = 'testpassword'

# Factory for UserAccount Model
class UserAccountFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    dob = '1992-04-25'
    bio = 'Test Bio'

    class Meta:
        model = UserAccount

# Factory for Post Model
class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    caption = factory.Faker('sentence')
    likes = factory.Faker('random_int', min=0, max=1000)

# Factory for Friends Model
class FriendsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friends
    friend_a = factory.SubFactory(UserFactory)
    friend_b = factory.SubFactory(UserFactory)
    chat = "test-chat"

# Factory FriendRequest Model
class FriendRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FriendRequest

    sender = factory.SubFactory(UserFactory)
    receiver = factory.SubFactory(UserFactory)
    status = "pending"

# Factory for Message Model
class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    chat = 'testchat'
    sender = factory.SubFactory(UserFactory)
    date_sent = factory.Faker('date')
    message = 'random_message'