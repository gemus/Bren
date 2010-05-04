from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.conf import settings

from crossfit.email_sender.models import UserEmailPermissions
from crossfit.email_sender.sender import email_user

def confirm(request, given_code):
    try:
        email_perm = UserEmailPermissions.objects.get(pk=given_code)
        email_perm.has_permission = True
        email_perm.save()
        return render_to_response('email_sender/confirm.html', {'email': email_perm.user.email})
    except UserEmailPermissions.DoesNotExist:
        data = dict(given_code=given_code)
        return render_to_response('email_sender/bad_confirm_code.html')
    
def unsubscribe(request, given_code):
    email_perm = UserEmailPermissions.objects.get(pk=given_code)
    email_perm.has_permission = False
    email_perm.save()
    return render_to_response('email_sender/unsubscribe.html', {'email': email_perm.user.email})

def send_perm_request(user):
    # Grab existing hash, or generate one
    email_perms = UserEmailPermissions.objects.filter(user=user)
    if len(email_perms) > 0:
        email_perm = email_perms[0]
    else:
        email_perm = UserEmailPermissions(user=user)
        email_perm.save()
    subscribe_hash = email_perm.subscribe_hash

    subscribe_url = "%semail/confirm/%s/" % (settings.CONFIRM_EMAIL_PERM_BASE_URL,
                                              subscribe_hash)

    email_user(user,
               "Permission Request",
               'email_sender/emails/perm_request.html',
               {"subscribe_url":subscribe_url})

    return render_to_response('email_sender/perm_sent.html')

    #return render_to_response(  'email_sender/emails/perm_request.html',
    #                           {"subscribe_url":subscribe_url})
