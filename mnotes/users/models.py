import hmac
import uuid
from hashlib import sha1

from django.contrib.auth.models import User
from django.db import models


def generate_key():
    new_uuid = uuid.uuid4()
    return hmac.new(str(new_uuid), digestmod=sha1).hexdigest()


class APIKey(models.Model):
    key = models.CharField(max_length=256, default=generate_key)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now=True)
