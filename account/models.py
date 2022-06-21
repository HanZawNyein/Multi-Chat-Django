from django.conf import settings
from django.db import models

# Create your models here.
from django.urls import reverse

from account.managers import ReceiverManager


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile")
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        Add a New Friend
        :param account:
        :return:
        """
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        """
        Remove A Friend
        :param account:
        :return:
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, remove):
        """
        Initial the action
        :param remove:
        :return:
        """
        remover_friends_list = self

        # remove friend list from remover friends list
        remover_friends_list.remove_friend(remove)

        # remove friend list from removed friends list
        friends_list = FriendList.objects.get(user=remove)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        """
        is this a friend
        :param frined:
        :return:
        """
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    """
    A Friend request consists of two main parts
        1. SENDER:
            - Person Sending the friend request
        2. RECEIVER:
            - Person receive the friend request

    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # The default manager.
    request_receiver = ReceiverManager()  # Our custom manager.

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        accept a friend
        update sender and receiver of friends list
        :return:
        """
        try:
            receiver_friend_list = FriendList.objects.get(user=self.receiver)
        except:
            receiver_friend_list = FriendList.objects.create(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            try:
                sender_friend_list = FriendList.objects.get(user=self.sender)
            except:
                sender_friend_list = FriendList.objects.create(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = True
                self.save()

    def decline(self):
        """Decline A Friend Request"""
        self.delete()

    def cancel(self):
        """"
        Cancel A Friend Request
        """
        self.delete()
        # self.is_active = False
        # self.save()
