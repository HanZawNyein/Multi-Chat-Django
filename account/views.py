from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import FriendRequest, FriendList
# Create your views here.
from django.views.decorators.http import require_http_methods

from account.forms import UserRegistrationForm


# from account.models import Friend


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm()
        if user_form.is_valid():
            print("post")
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # return  #render(request, 'account/register_done.html', {"new_user": new_user})
        else:
            print(user_form.errors)
            messages.error(request, "error")
            for field in user_form:
                for error in field.errors:
                    print(error)
                    messages.error(request, error)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {"user_form": user_form})


@login_required
def profile(request):
    return render(request, 'account/profile/posts.html')


@login_required
def add_friend(request):
    all_friends = request.user.friends.all()
    users = User.objects.all().exclude(username__in=[fri.user.username for fri in all_friends])
    users = users.exclude(username=request.user.username)
    context = {
        "users": users,
    }
    return render(request, 'account/friends/add_friends.html', context)


@require_http_methods(["POST"])
def request_a_friend(request, user_id):
    request_friend = FriendRequest.objects.create(sender=request.user, receiver_id=user_id)
    request_friend.accept()
    return redirect("add_friends")


def all_friend_requests(request):
    friend_requests = FriendRequest.request_receiver.all_requests(request.user)
    context = {
        "friend_requests": friend_requests
    }
    return render(request, 'account/friends/friend_requests.html', context)


@require_http_methods(["POST"])
def request_a_friend_cancel(request, user_id):
    cancel_request = FriendRequest.objects.get(sender=request.user, receiver_id=user_id)
    cancel_request.cancel()
    return redirect("add_friends")


@require_http_methods(["POST"])
def request_a_friend_decline(request, user_id):
    print(user_id, request.user)
    cancel_request = FriendRequest.objects.get(sender_id=user_id, receiver=request.user)
    cancel_request.cancel()
    return redirect("all_friend_requests")


def all_friend(request):
    all_friends = request.user.friends.all()
    context = {
        "all_friends": all_friends
    }
    return render(request, 'account/friends/all_friends.html', context)
