from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=256, blank=True)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    updated = models.DateTimeField(auto_now=True)
