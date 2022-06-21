from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from account.models import FriendList
from .models import Room
from .random_generator import random_number


def Convert(lst):
    res_dct = {{lst[i]: lst[i + 1]} for i in range(0, len(lst), 2)}
    return res_dct


# Create your views here.
@login_required
def all_messages(request, course_id=None):
    friends = request.user.friends.all()
    rooms = Room.objects.filter(friends=request.user)
    rooms_for_list = []
    context = {}
    for a in friends:
        try:
            room = rooms.get(friends=a.user.id)
        except:
            room = Room.objects.create(room_number=random_number())
            room.friends.add(a.user, request.user)
            room.save()
        rooms_for_list.append({"user": a.user, "room_number": room})
    context = {
        "all_friends": rooms_for_list
    }
    if course_id:
        context["course_id"] = course_id
    return render(request, 'chat/components/chatwidget.html', context=context)
