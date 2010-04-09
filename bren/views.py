import datetime

from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

import crossfit.bren.models as model

# =============================================================================
# = Index Page ================================================================
# =============================================================================
@login_required
def index(request):
    data = {'display_name': "%s %s" % (request.user.first_name, request.user.last_name),
            'cur_date_str': datetime.datetime.now().strftime("%A %B %d %Y").replace(' 0', ' ')}
    return render_to_response('bren/index.html', data)

# =============================================================================
# = Workout Form ==============================================================
# =============================================================================
class WorkoutForm(forms.Form):
    def __init__(self, elements, *args, **kw):
        super(WorkoutForm, self).__init__(*args, **kw)
        for field_dict in elements:
            # In the style of 'varient_<element_id>_<order_num>'
            field_id = "varient_%d_%d" % (field_dict['element']['id'], field_dict['order'])

            if field_dict['element']['type'] == "weight":
                field = forms.CharField()
            else:
                field = forms.ChoiceField()
                field.choices = [ (varient['id'], varient['name']) for varient in field_dict['element']['variations']]
            if not field_dict['reps'] == 1:
                field.label = "%d %s" % (field_dict['reps'], field_dict['element']['name'])
            else:
                field.label = field_dict['element']['name']

            self.fields[field_id] = field

@login_required
def workout_form(request, date_str, class_id):
    api_data = model.get_workout(date_str, class_id)
    initial_time_reps = None
    previous_data = model.get_workout_variations(request.user.id, api_data['workout_class'])
    the_form = WorkoutForm(api_data['elements'], previous_data)
    workout = model.user_done_class(request.user.id, api_data['id'], date_str)
    if not workout == None:
        workout_type = workout.workout_class.workout.workout_type
        if workout_type == "Timed":
            time = workout.secs
            mins = time / 60
            secs = time % 60
            initial_time_reps = "%d:%02d" % (mins, secs)
        elif workout_type == "AMRAP":
            initial_time_reps = workout.rounds

    ele_history = model.get_workout_element_history(request.user.id, api_data['id'])
    co_list = model.get_completed_workout(request.user.id, api_data['id'])

    for workout in co_list:
        OUTPUT_FORMAT = "%B %d, %Y" # December 1, 2009
        workout_date = datetime.datetime.strptime(workout['date'], model.DATE_FORMAT)
        workout['date'] = workout_date.strftime(OUTPUT_FORMAT).replace(' 0', ' ')

        if workout['info']['type'] == "Timed":
            time = workout['info']['time']
            mins = time / 60
            secs = time % 60
            workout['info']['time'] = "%d:%02d" % (mins, secs)
    data = {
        'name':         api_data['name'],
        'comments':     api_data['comments'],
        'workout_type': api_data['workout_type'],
        'class_name':   api_data['class_name'],
        'rounds':       api_data['rounds'],
        'time':         api_data['time'],
        'user_id' :     request.user.id,
        'date_str':     date_str,
        'class_id':     class_id,
        'the_form':     the_form,
        'co_list' :     co_list,
        'ele_history':  ele_history,
        'initial_time_reps': initial_time_reps,
    }

    return render_to_response('bren/workout_form.html', data)

@login_required
def save_workout(request):
    # Basic Information
    date_str = request.POST.get('date_str')
    class_id = request.POST.get('class_id')

    varient_list = []
    varient_keys = [x for x in request.POST.keys() if x[:8] == 'varient_']
    for key in varient_keys:
        parts = key.split('_')
        element_id = parts[1]
        order = parts[2]
        varient_id = request.POST.get(key)
        varient_list.append({"order": int(order), "variation_id": int(varient_id), "element_id": int(element_id) })

    # Deal with rounds and time
    workout_type = request.POST.get('workout_type')
    if workout_type == "AMRAP":
        workout_rounds = request.POST.get('workout_reps')
        workout_time = model.get_workout_with_date_class(date_str, class_id)['time']
    elif workout_type == "Timed":
        workout_rounds = model.get_workout_with_date_class(date_str, class_id)['rounds']
        time_parts = request.POST.get('workout_time').split(":")
        workout_time = int(time_parts[0]) * 60 + int(time_parts[1])
    elif workout_type == "Done":
        workout_rounds = 1
        workout_time = 0

    save_dict = {
        "time":       workout_time,
        "rounds":     workout_rounds,
        "date":       date_str,
        "class_id":   class_id,
        "variations": varient_list,
        "user_id":    request.user.id
    }

    model.create_completed_workout(save_dict);
    HTTP_REFERER = request.META['HTTP_REFERER']
    return render_to_response('bren/save_workout.html', {'HTTP_REFERER': HTTP_REFERER})

@login_required
def no_workout_found(request, date, *args):
    OUTPUT_FORMAT = "%A %B %d, %Y" # December 1, 2009
    the_date = datetime.datetime.strptime(date, model.DATE_FORMAT)
    the_date = the_date.strftime(OUTPUT_FORMAT).replace(' 0', ' ')
    return render_to_response('bren/no_workout_found.html', {"date": the_date})

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
