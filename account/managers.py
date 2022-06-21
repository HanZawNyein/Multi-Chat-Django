from django.db import models

class ReceiverManager(models.Manager):
    def all_requests(self, receiver):
        return super(ReceiverManager, self).get_queryset().filter(receiver=receiver, is_active=False)
