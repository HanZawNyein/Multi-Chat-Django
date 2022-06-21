from django.conf import settings
from django.db import models
from . random_generator import random_number


# Create your models here.
class Room(models.Model):
    room_number = models.IntegerField(default=random_number())
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="rooms")

    def __str__(self):
        return str(self.room_number)
