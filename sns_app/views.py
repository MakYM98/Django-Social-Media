from django.shortcuts import render
from .models import *
from .forms import *
from .serializers import *
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from django.db.models import Q
import json
from django.utils.timezone import now
from django.forms.models import model_to_dict

# View for New Account Registration
def register(request):
    registered = False
    # If request method is POST, check if form is valid then save account
    if request.method == 'POST':
        # Pass Post Data to Django Forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        # Form Validation
        if user_form.is_valid() and profile_form.is_valid(): 
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered=True
    # If request method is GET, return Forms for users to fill in.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'snsApp/signup.html', {'user_form': user_form, 
                                                  'profile_form':profile_form, 
                                                  'registered':registered})

# View for User Login
def user_login(request):
    # If Request method is POST, authenticate to see if username exists and
    # password is matches the one in the database.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # If user credentials is correct and account is active, redirect them
        #  to the account homepage.
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disable")
        else:
            return render(request, 'snsApp/login.html', {'error':"Invalid"})
    return render(request, 'snsApp/login.html', {})

# View for Users to Log out
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

# View for Users edit their profile details
@login_required
def edit_profile(request):
    user = request.user
    if user.is_authenticated:
        # Retrieve all user details such as Profile images and username.
        user_profile = UserAccount.objects.get(user=user)
        if user_profile.profile_image:
            image_url = user_profile.profile_image.url
            old_image_url = user_profile.profile_image.path
        else:
            image_url= None
            old_image_url = None
        # If request method is POST, means users changed their account details.
        if request.method == "POST":
            # Pass the form data to the UserFormUpdate
            user_form = UserFormUpdate(request.POST or None, instance=user)
            user_profile_form = UserProfileFormUpdate(request.POST or None, 
                                                        request.FILES, 
                                                        instance=user_profile)
            # Form Validation
            if user_form.is_valid() and user_profile_form.is_valid():
                user_form.save()
                if user_profile.profile_image:
                    new_image_url = user_profile.profile_image.path
                    if old_image_url==new_image_url:
                        user_profile_form.save()
                    elif old_image_url==None:
                        user_profile_form.save()
                    else:
                        os.remove(old_image_url)
                        user_profile_form.save()
                else:
                    user_profile_form.save()
                return HttpResponseRedirect('/user_home')
        # If request method is not POST, display original details on form.
        else:
            user_form = UserFormUpdate(instance=user)
            user_profile_form = UserProfileFormUpdate(instance=user_profile)
    # If user not logged in, redirect them back to login
    else:
        return HttpResponseRedirect('/login')

    return render(request, "snsApp/edit_profile.html", 
                  {"user":user, "user_profile":user_profile, 
                   "img_url":image_url, "user_form":user_form, 
                   "profile_form":user_profile_form})

# View for Home Feed of User that is logged in
@login_required
def user_profile(request):
    user = request.user
    # Check if user is logged in
    if user.is_authenticated:
        # Grab user details
        user_profile = UserAccount.objects.get(user=user)
        if user_profile.profile_image:
            img_url = user_profile.profile_image.url
        else:
            img_url = None
        # If Request Method is POST, means users are creating a new POST
        if request.method=="POST":
            # Pass POST data to New Post Form
            post_form = NewPostForm(request.POST, request.FILES)
            # Form Validation
            if post_form.is_valid(): 
                post_form.save(user=user, time=datetime.now())
        else:
            # If request method is NOT POST, return empty form
            post_form = NewPostForm()

        # Get User's Post sorted by when it was sorted
        # Using Post_id because it reflects which post was first.
        post = Post.objects.filter(user=user).order_by('-post_id')
        # Rearrange the array so that it can be used to display in rows of 3
        postList = [post[i:i+3] for i in range(0, len(post), 3)]
        userObj = User.objects.get(username=user)
        # Get number of friends that the user has
        # Using Q Function to get objects that either Friend A/B is user
        friend_count = Friends.objects.filter(Q(friend_a=userObj) | 
                                              Q(friend_b=userObj)).count()
    else:
        return HttpResponseRedirect('/login')
        
    return render(request, "snsApp/user_profile.html", 
                  {"user_profile":user_profile, "img_url":img_url, 
                   "post_form":post_form, "posts":postList, 
                   "follower_count":friend_count})

# View for Users to Create a New Post
@login_required
def create_post(request):
    user = request.user
    # Get User Details
    user_profile = UserAccount.objects.get(user=user)
    # Check that user has logged in
    if user.is_authenticated:
        # If Request Method is POST, pass request data to New Post Form
        if request.method=="POST":
            post_form = NewPostForm(request.POST, request.FILES)
            # Form Validation
            if post_form.is_valid(): 
                post_form.save(user=user, time=datetime.now())
        else:
            post_form = NewPostForm()
    else:
        return HttpResponseRedirect('/login')
        
    return render(request, "snsApp/new_post.html", 
                  {"user_profile":user_profile, "post_form":post_form})

# View for users to see the list of Friend Requests
@login_required
def friend_request(request):
    user = request.user
    # Get User details
    user_profile = UserAccount.objects.get(user=user)
    # If Request Method is POST, update the status of the request based on 
    # the action provided in the POST data.
    if request.method=="POST":
        post_data = dict(request.POST.lists())
        receiver = post_data['receiver'][0]
        sender = post_data['sender'][0]
        action = post_data['action'][0]
        # Get Sender & Receiver User objects
        req_sender = User.objects.get(username=sender)
        req_receiver = User.objects.get(username=receiver)
        # If Action is Accept, delete the Friend Request Object and
        # Create a new Friends object with both the users.
        if action == 'accept':
            FriendRequest.objects.filter(sender=req_sender, 
                                            receiver=req_receiver).delete()
            
            chat_room = str(sender) + str(receiver) + 'chat'
            friend_obj = Friends(
                    friend_a = req_sender,
                    friend_b = req_receiver,
                    chat = chat_room
                )
            friend_obj.save()
        # If Action is Decline, delete the Friend Request Object
        elif action == 'decline':
            FriendRequest.objects.filter(sender=req_sender, 
                                         receiver=req_receiver).delete()
        return render(request, "snsApp/friend_request.html")
    # If Request Method is GET, get all request with user as receiver 
    elif request.method=="GET":
        requests = FriendRequest.objects.all().filter(receiver=user)

        return render(request, "snsApp/friend_request.html", 
                      {
                            "requests":requests, 
                            'user_profile':user_profile
                        })
    else:
        return render(request, "snsApp/friend_request.html")

# API View for Other Users that is not the Logged In Users
class OtherUsers(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "snsApp/other_user_profile.html"
    # Function for GET request
    def get(self, request, username): 
        # Get Other User's User Object
        
        otherUser = User.objects.get(username=username)
        loggedUser = User.objects.get(username=request.user)
        user_profile = UserAccount.objects.get(user=loggedUser)
        # Declare conditions to grab Friend Objects
        friend_criteria_one = (Q(friend_a=otherUser) & 
                                Q(friend_b=loggedUser))
        friend_criteria_two = (Q(friend_a=loggedUser) & 
                                Q(friend_b=otherUser))
        # Combine both conditions
        friend_obj = Friends.objects.filter(
                        friend_criteria_one | friend_criteria_two
                    )
        # Using Q Function to get objects that either Friend A/B is user
        # If object exists, means Other User and Logged In User are Friends
        if friend_obj:
            following=True
        else:
            # If Users are not friends, logged in User has sent a friend request
            if FriendRequest.objects.filter(sender=loggedUser, receiver=otherUser):
                following='Requested'
            else:
                following=False
        # Retrieve Other User's information
        user = UserSerializer(otherUser)
        if otherUser.profile.profile_image:
            img_url = user.data['profile']['profile_image']
        else:
            img_url = None
        # Retrieve Other User's Friend Count
        friend_count = Friends.objects.filter(Q(friend_a=otherUser) | 
                                              Q(friend_b=otherUser)).count()
        # Rearrange Other User's Posts to display as rows of 3
        print(user_profile)
        postList = [user.data['posts'][i:i+3] for i in range(0, len(user.data['posts']), 3)]
        return Response({"subuser":otherUser, "user_profile": user_profile, 
                         "img_url": img_url, "posts":postList, 
                         "friend_count":friend_count, "following":following,
                         "user_profile":user_profile})
    
    # Function for POST request
    def post(self, request, username):
        # Get Other User's User Object
        otherUser = User.objects.get(username=username)
        user = UserSerializer(otherUser)
        loggedUser = User.objects.get(username=request.user)
        user_profile = UserAccount.objects.get(user=loggedUser)

        # Retrieve Other User's information
        if otherUser.profile.profile_image:
            img_url = user.data['profile']['profile_image']
        else:
            img_url = None
        # Declare a Temporary Friend Request Status
        following = 'In Progress'
        # Send Request/Retract Request/Unfriend
        if request.method=="POST": 
            # Check if both Users are Friends
            # Declare conditions to grab Friend Objects
            friend_criteria_one = (Q(friend_a=otherUser) & 
                                   Q(friend_b=loggedUser))
            friend_criteria_two = (Q(friend_a=loggedUser) & 
                                   Q(friend_b=otherUser))
            # Combine both conditions
            friend_obj = Friends.objects.filter(
                            friend_criteria_one | friend_criteria_two
                        )
            # Declare conditions to grab Friend Request Objects
            req_criteria_one = (Q(sender=otherUser) & 
                                   Q(receiver=loggedUser))
            req_criteria_two = (Q(sender=loggedUser) & 
                                   Q(receiver=otherUser))
            # Combine both conditions
            req_obj = FriendRequest.objects.filter(
                            req_criteria_one | req_criteria_two
            )

            # If Friend object exists, delete
            if friend_obj:
                friend_obj.delete()
                following=False
            # If Friend Request object exists, delete
            elif req_obj:
                FriendRequest.objects.filter(sender=loggedUser, 
                                             receiver=otherUser).delete()
                following=False
            # If no existing Request and they are not friends, send a request
            else:
                # Create a new Friend Request 
                request_serializer = FriendRequest(
                    sender= loggedUser,
                    receiver= otherUser,
                    status='Pending'
                )
                request_serializer.save()
                following='Requested'
            # Rearrange the array so that it can be used to display in rows of 3
            postList = [user.data['posts'][i:i+3] for i in range(0, len(user.data['posts']), 3)]
            friend_count = Friends.objects.filter(Q(friend_a=otherUser) | 
                                              Q(friend_b=otherUser)).count()
            return Response({"subuser":otherUser, "user_profile": 
                             user.data['profile'], "img_url": img_url, 
                             "posts":postList,"following":following,
                            "friend_count": friend_count,
                             "user_profile":user_profile})

# View to display search results
def user_search(request):
    #  Get Logged In User's Details
    user_profile = UserAccount.objects.get(user=request.user)
    if request.method == "POST":
        search = request.POST['q']
        if search:
            # Return all user object that contains the search keyword
            result = User.objects.filter(username__contains=search)
            images = []
            # For each User filtered, get the User's Detail
            for user in result:
                profile_result=UserAccount.objects.get(user=user)
                if profile_result.profile_image:
                    profile_img = profile_result.profile_image.url
                    images.append(profile_img)
                else:
                    images.append(None)
            search_result = zip(result, images)
            return render(request, "snsApp/search_user.html",
                          {'search_result':search_result, 
                           'user_profile':user_profile,
                           'logged_user':request.user})
        else:
            return render(request, 'snsApp/search_user.html')
    else:
        return HttpResponseRedirect("/")

# View to see a list of Friends
def friend_list(request):
    # Get Logged in User's Details
    user_profile = UserAccount.objects.get(user=request.user)
    user_obj = User.objects.get(username=request.user)
    # Get List of Friends
    if request.method == "GET":
        friend_list=[]
        # Get User's List of Friends and Friend Count
        friends = Friends.objects.filter(Q(friend_a=user_obj) | 
                                         Q(friend_b=user_obj))
        friend_count = len(friends)
        # Create a list of friend's names
        for friend in friends:
            if str(friend.friend_a) == str(user_profile.user):
                friend_list.append(friend.friend_b)
            else:
                friend_list.append(friend.friend_a)
        # Get Friend's User Object
        user_list = User.objects.all().filter(username__in=friend_list)
        user_acc = UserAccount.objects.all().filter(user_id__in=user_list)

        return render(request, "snsApp/friend_list.html", {
                "friend_list":user_acc, 
                "friend_count":friend_count, 'user_profile':user_profile
            })
    else:
        return HttpResponseRedirect("user_home/")

# API View for Home Feed
class HomeFeedView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'snsApp/home_base.html'
    # Function for GET Request
    def get(self, request):
        user = request.user
        # If not logged in, redirect to login page
        if not user.is_authenticated:
            return HttpResponseRedirect('/login')
        
         # Get Logged in User's Details
        user_obj = User.objects.get(username=user)

        # Get User's List of Friends
        friend_list = []
        friends = Friends.objects.filter(Q(friend_a=user_obj) | 
                                         Q(friend_b=user_obj))
        # Iterate through friends list to create a list of User objects
        for friend in friends:
            friendModel = model_to_dict(friend)
            friend_a = User.objects.get(id=friendModel['friend_a'])
            friend_b = User.objects.get(id=friendModel['friend_b'])
            print(friend_a)
            print(friend_b)
            if str(user) == str(friend_a.username):
                print(friend_b)
                friend_list.append(friend_b)
            else:
                print(friend_a)
                friend_list.append(friend_a)
        print(friend_list)
        friend_list.append(User.objects.get(username=user))
        # The list of user objects will be used to get ALL posts for home feed
        # Retrieve all POSTS based on logged in User's Post and User's Friends
        post = Post.objects.filter(user__in=friend_list).order_by('-post_id')
        # Rearrange Posts to rows of 3
        postList = [post[i:i+3] for i in range(0, len(post), 3)]

        if user.is_authenticated:
            user_profile = UserAccount.objects.get(user=user)
            following_list=[]
            followings = Friends.objects.filter(Q(friend_a=user_obj) | 
                                                Q(friend_b=user_obj))
            for following in followings:
                following_list.append(following)
            if user_profile.profile_image:
                image_url = user_profile.profile_image.url
            else:
                image_url = None

            return Response({'posts':postList, 'user_profile':user_profile, 
                             'img_url':image_url, 'user':user,
                             'following_list':following_list})
            
        
        return Response({'posts':postList, 'user_profile':None, 'img_url':None, 
                         'user':user,'following_list':None})

# View for Chat Room
@login_required
def chat_room(request, room_name):
    # Get Logged in User's Details
    user_profile = UserAccount.objects.get(user=request.user)
    # Check if user has profile image
    if user_profile.profile_image:
        image_url = user_profile.profile_image.url
    else:
        image_url = ''
    # Get All Past Messages based on Chat Room Name
    messages = [] 
    # Filter Messages based on Chat Room Name
    if Message.objects.filter(chat=room_name):
        # Sort the Messages by date and time
        messageModel = Message.objects.filter(chat=room_name).order_by('date_sent')
        # Create a list of messages
        for m in messageModel:
            model_dict = model_to_dict(m)
            senderObj = User.objects.get(id=model_dict['sender'])
            messages.append({
                'message':model_dict['message'],
                'sender':model_to_dict(senderObj)['username']
            })

    return render(request, "snsApp/chat_room.html", {
                            'room_name':room_name, 
                            "username":str(request.user), 
                            'user_profile':user_profile,
                            'img_url':image_url,
                            # 'following_list':friend_list,
                            'messages':json.dumps(messages)
                            })

# View for List of Chats
def chat_list(request):
    user_profile = UserAccount.objects.get(user=request.user)
    if request.method == "GET":
        # Get All Logged In User's Friends
        friend_list=[]
        friends = Friends.objects.filter(Q(friend_a=request.user) | 
                                         Q(friend_b=request.user))
        friend_count = len(friends)
        for user in friends:
            friend_list.append(user)
        return render(request, "snsApp/chat_list.html", {
                "friend_list":friend_list, 
                "friend_count":friend_count,
                "loggedUser":request.user,
                "user_profile":user_profile
            })
    else:
        return HttpResponseRedirect("user_home/")

# Save Messages
def save_message(request):
    request_data = json.loads(request.body)
    # Create Message Object
    if request.method == 'POST':
        message = Message(
            chat=request_data['chat'],
            message=request_data['message'],
            sender=User.objects.get(username=request_data['sender'])
        )

        message.save()
        
    return HttpResponse('Success')

# Unfriend Users
def unfriend(request):
    request_data = request.POST
    loggedUser = User.objects.get(username = request_data['user'])
    otherUser = User.objects.get(username = request_data['friend'])

    criteria_one = (Q(friend_a=loggedUser) & 
                    Q(friend_b=otherUser))
    criteria_two = (Q(friend_a=otherUser) & 
                    Q(friend_b=loggedUser))

    # Delete Users
    if request.method == 'POST':
        # Get Friend Object and Delete the object
        instance = Friends.objects.get(criteria_one | criteria_two)
        instance.delete()
    return HttpResponseRedirect("/user_home/")

# View for Other User's Friend List
def user_friend_list(request, username):
    user = User.objects.get(username=username)
    user_profile = UserAccount.objects.get(user=user)
    logged_user_profile = UserAccount.objects.get(user=request.user)

    if request.method == "GET":
        # All Other User's Friends
        friend_list=[]
        friends = Friends.objects.filter(Q(friend_a=user) | 
                                         Q(friend_b=user))
        friend_count = len(friends)
        # Create a list of Other User's Friends names
        for friend in friends:
            if str(friend.friend_a) == str(user_profile.user):
                friend_list.append(friend.friend_b)
            else:
                friend_list.append(friend.friend_a)
        # Create a list of User Objects based on the friend list
        user_list = User.objects.all().filter(username__in=friend_list)
        user_acc = UserAccount.objects.all().filter(user_id__in=user_list)
        return render(request, "snsApp/friend_list.html", {
                    "friend_list":user_acc, 
                    "friend_count":friend_count, 'user_profile':user_profile,
                    'loggedUser':request.user,
                    'user_profile':logged_user_profile
                })
    else:
        return HttpResponseRedirect("user_home/")