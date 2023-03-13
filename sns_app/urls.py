from django.urls import include, path
from . import views
from . import api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Path for Home Feed Page
    path('', views.HomeFeedView.as_view(), name='home'),
    # Path for Sign Up Page
    path('signup/', views.register, name='signup' ),
    # Path for Login Page
    path('login/', views.user_login, name='login'),
    # Path for Logout Page
    path('logout/', views.user_logout, name='logout'),
    # Path for Edit Profile Page
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    # Path for Logged in User Profile Page
    path('user_home/', views.user_profile, name='user_profile'),
    # Path for Creating New Post
    path('new_post/', views.create_post, name='create_post'),
    # Path for viewing Friend List
    path('friend_list/', views.friend_list, name='friend_list'),
    # Path for viewing Friend Request List
    path('friend_request/', views.friend_request, name='friend-request'),
    # Path for viewing Other User's Profile
    path('profile/<str:username>/', views.OtherUsers.as_view(), 
         name='other_users'),
    # Path for viewing Other User's Friends
    path('profile/<str:username>/friends/', views.user_friend_list, 
         name='user-friends'),
    # Path for viewing Search Results
    path('search_user', views.user_search, name='search-user'),
    # Path for Chat Room
    path('chat/<str:room_name>/', views.chat_room, name='chat-room'),
    # Path for viewing list of chats
    path('chat_list/', views.chat_list, name='chat_list'),
    # Path for saving messages
    path('save_message/', views.save_message, name='save_message'),
    # Path for getting User Details
    path('api/user/<str:username>/', api.UserList.as_view(), name='user_list'),
    # Path for getting Post Details
    path('api/posts/<int:pk>/', api.PostsList.as_view(), name='post'),
    # Path for creating New Post 
    path('api/post/', api.NewPostList.as_view(), name='new_post'),
    # Path for deleting Friend
    path('unfriend/', views.unfriend, name='unfriend'),
     # For Automatic Page reloads
    path("__reload__/", include("django_browser_reload.urls")),
]

# urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
