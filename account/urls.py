from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('login/', LoginView.as_view(), name="login"),
    path('lgout/', LogoutView.as_view(), name="logout"),

    path('register/', views.register, name='register'),

    path('profile/', views.profile, name="profile"),
    path('add-friends/', views.add_friend, name="add_friends"),
    path('request-a-friend/<int:user_id>/', views.request_a_friend, name="request_a_friend"),
    path('request-a-friend-cancel/<int:user_id>/', views.request_a_friend_cancel, name="request_a_friend_cancel"),
    path('request-a-friend-decline/<int:user_id>/', views.request_a_friend_decline, name="request_a_friend_decline"),
    path('all-friend-requests/', views.all_friend_requests, name="all_friend_requests"),
    path('all-friends/', views.all_friend, name="all_friends"),
]
