from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.models import User

import crossfit.bren.models as model
import crossfit.email_sender.models as email_sender_model
import crossfit.email_sender.views

# =============================================================================
# = API Endpoint ==============================================================
# =============================================================================
def json_api(request):
    """ JSON API Endpoint --
    Request  : { id: <int>, method: <string>, params: [parameters] }
    Response : { id: <int>, result: <object>, error: <object> }
    """

    # TODO : Ensure all are using proper JSON
    #      : Validate request
    #      : Require permission for certain calls
    #      : Clean up this ugly elseif business

    method = request.GET['method']

    to_return = {
        "id"     : request.GET['id'],
        "result" : None,
        "error"  : "Bad Method Specified '%s'" % method
    }

    if method == 'get_classes':
        result = model.get_classes(request.GET['params'])['workout_class_list']
        to_return = {
            "id"     : request.GET['id'],
            "result" : result,
            "error"  : None
        }
    elif method == 'get_users':
        json_params = simplejson.loads(request.GET['params'])
        if len(json_params) == 2:
            result = model.get_users(json_params[0], json_params[1])
        if len(json_params) == 3:
            result = model.get_users(json_params[0], json_params[1], json_params[2])    
            
        to_return = {
            "id"     : request.GET['id'],
            "result" : result,
            "error"  : None
        }
    elif method == 'get_user':
        json_params = simplejson.loads(request.GET['params'])
        result = model.get_user(json_params[0])
        to_return = {
            "id"     : request.GET['id'],
            "result" : result,
            "error"  : None
        }
    elif method == 'check_user_login':
        json_params = simplejson.loads(request.GET['params'])
        username, password = json_params
        result = model.check_user_login(username, password)
        to_return = {
            "id"     : request.GET['id'],
            "result" : result,
            "error"  : None
        }
    elif method == 'update_user':
        json_params = simplejson.loads(request.GET['params'])
        result = model.update_user(json_params[0])
        error_result = None
        if result[:4] == 'fail':
            error_result = result
            result = None
        to_return = {
            "id"     : request.GET['id'],
            "result" : result,
            "error"  : error_result
        }
    elif method == 'create_user':
        json_params = simplejson.loads(request.GET['params'])
        result = model.create_user(json_params[0])
        error_result = None
        to_return = {
            "id"     : request.GET['id'],
            "result" : result,
            "error"  : error_result
        }
    elif method == 'delete_user':
        json_params = simplejson.loads(request.GET['params'])
        result = model.delete_user(json_params[0]['user_name'])
        error_result = None
        to_return = {
            "id"     : request.GET['id'],
            "result" : result,
            "error"  : error_result
        }
    elif method == 'has_email_permission':
        json_params = simplejson.loads(request.GET['params'])
        user = User.objects.get(username__exact=json_params[0]['user_name'])
        result = email_sender_model.can_email_user(user)
        error_result = None
        to_return = {
            "id"     : request.GET['id'],
            "result" : result,
            "error"  : error_result
        }
    elif method == 'send_permission_request':
        json_params = simplejson.loads(request.GET['params'])
        user = User.objects.get(username__exact=json_params[0]['user_name'])
        crossfit.email_sender.views.send_perm_request(user)
        error_result = None
        to_return = {
            "id"     : request.GET['id'],
            "result" : "success",
            "error"  : error_result
        }
    elif method == 'remove_permission_request':
        json_params = simplejson.loads(request.GET['params'])
        user = User.objects.get(username__exact=json_params[0]['user_name'])
        email_sender_model.remove_permission_request(user)
        error_result = None
        to_return = {
            "id"     : request.GET['id'],
            "result" : "success",
            "error"  : error_result
        }

    return HttpResponse(simplejson.dumps(to_return))