from django.urls import reverse
from djongo import models

from django.utils import timezone


# Create your models here.
class UserObject(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    activate = models.BooleanField(default=True)
    last_update = models.DateTimeField(default=timezone.now)

    medias = models.JSONField(blank=True, null=True, default={})
    stories = models.JSONField(blank=True, null=True, default={})

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_url', kwargs={'username': self.username, 'resource': 'all', 'filter':  'objects'})

    def get_delete_url(self):
        return reverse('delete_url', kwargs={'username': self.username})
