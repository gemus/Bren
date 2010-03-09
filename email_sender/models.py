from random import random

from django.contrib.auth.models import User
from django.db import models
from django.utils.hashcompat import sha_constructor

def gen_subscribe_hash():
    return sha_constructor(str(random())).hexdigest()[:10]

class UserEmailPermissions(models.Model):
    subscribe_hash = models.CharField(max_length=20, primary_key=True, default=gen_subscribe_hash)

    user = models.ForeignKey(User, unique=True)
    has_permission = models.BooleanField(default=False)
