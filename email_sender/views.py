from django.shortcuts import render_to_response

from crossfit.email_sender.models import UserEmailPermissions

def confirm(request, given_code):
    try:
        email_perm = UserEmailPermissions.objects.get(pk=given_code)
        data = dict(given_code=given_code)
        return render_to_response('email_sender/confirm.html', data)
    except UserEmailPermissions.DoesNotExist:
        data = dict(given_code=given_code)
        return render_to_response('email_sender/bad_confirm_code.html', data)
