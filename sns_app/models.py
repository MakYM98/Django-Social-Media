from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Model for User Details which serves as an extension to Django's User Model
class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
                                related_name="profile")
    profile_image = models.ImageField(upload_to='images_profile', null=True, 
                                      blank=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=400, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

# Model of User's Posts
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, 
                             related_name='posts')
    post_date = models.DateField(null=True)
    caption = models.CharField(max_length=500)
    likes = models.IntegerField(null=True)
    image = models.ImageField(upload_to='post_images')

# Model to store Friends between Users
class Friends(models.Model):
    friend_a = models.ForeignKey(
            User, on_delete=models.DO_NOTHING, related_name='friend_a', 
            null=True)
    friend_b = models.ForeignKey(
            User, on_delete=models.DO_NOTHING, related_name='friend_b', 
            null=True)
    chat = models.CharField(max_length=100, null=True)

# Model to store Friend Request between Users
class FriendRequest(models.Model):
    sender = models.ForeignKey(
            User, on_delete=models.DO_NOTHING, related_name='freq_sender')
    receiver = models.ForeignKey(
            User, on_delete=models.DO_NOTHING, related_name='freq_receiver')
    status = models.CharField(max_length=100, null=True)

# Model to store Messages between Users
class Message(models.Model):
    chat = models.CharField(max_length=255, null=True)
    sender= models.ForeignKey(
            User, on_delete=models.DO_NOTHING, related_name='msg_sender')
    date_sent = models.DateTimeField(default=now)
    message = models.CharField(max_length=255, null=True)