from random import random

from django.contrib.auth.models import User
from django.db import models
from django.utils.hashcompat import sha_constructor

def gen_subscribe_hash():
    return sha_constructor(str(random())).hexdigest()[:10]

def can_email_user(user):
    if user.email and user.email != u'':
        return UserEmailPermissions.objects.filter(user = user).filter(has_permission = True).count() == 1
    return False

def remove_permission_request(user):
    UserEmailPermissions.objects.filter(user=user).delete()

def get_subscribed_users():
    return [i.user for i in UserEmailPermissions.objects.filter(has_permission=True)]

class UserEmailPermissions(models.Model):
    subscribe_hash = models.CharField(max_length=20, primary_key=True, default=gen_subscribe_hash)
    user = models.ForeignKey(User, unique=True)
    has_permission = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s" % (self.user, self.has_permission)
