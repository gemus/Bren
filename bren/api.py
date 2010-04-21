from django.http import HttpResponse
from django.utils import simplejson

import crossfit.bren.models as model
# =============================================================================
# = API Endpoint ==============================================================
# =============================================================================
def json_api(request):
    """ JSON API Endpoint --
    Request  : { id: <int>, method: <string>, params: [parameters] }
    Response : { id: <int>, result: <object>, error: <object> }
    """

    # TODO : Ensure all are using proper JSON

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
        result = model.get_users(json_params[0], json_params[1])
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
        if result[:4] == 'fail':
            error_result = result
            result = None
        to_return = {
            "id"     : request.GET['id'],
            "result" : result,
            "error"  : error_result
        }
    elif method == 'delete_user':
        print request.GET['params']
        json_params = simplejson.loads(request.GET['params'])
        result = model.delete_user(json_params[0]['user_name'])
        error_result = None
        if result[:4] == 'fail':
            error_result = result
            result = None
        to_return = {
            "id"     : request.GET['id'],
            "result" : result,
            "error"  : error_result
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

    return HttpResponse(simplejson.dumps(to_return))