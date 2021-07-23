#from django.db import models
from django.urls import reverse
from djongo import models

# Create your models here.
class UserObject(models.Model):
    username    = models.CharField(primary_key=True, max_length=50)
    activate    = models.BooleanField(default=True)

    medias      = models.JSONField(blank=True, null=True, default={})
    stories     = models.JSONField(blank=True, null=True, default={})

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_url', kwargs={'username': self.username})