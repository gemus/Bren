from django.shortcuts import render_to_response
from django import forms
import Crossfit.Bren.models as model
from django.http import HttpResponse
from django.utils import simplejson

# =============================================================================
# = Index Page ================================================================
# =============================================================================

def index(request):
    return render_to_response('index.html')

# =============================================================================
# = Workout Form ==============================================================
# =============================================================================

class WorkoutForm(forms.Form):

    def __init__(self, elements, *args, **kw):
        super(WorkoutForm, self).__init__(*args, **kw)
        for i, field_dict in enumerate(elements):
            field = forms.ChoiceField()
            field.choices = [ (varient['id'], varient['name']) for varient in field_dict['element']['variations']]

            field.label = "%d %s" % (field_dict['reps'], field_dict['element']['name'])
            self.fields['extra_info_%d' % i] = field

def workout_form(request, date_str, class_id):
    api_data = model.get_workout(date_str, class_id)
    the_form = WorkoutForm(api_data['elements'])

    data = {
        'name':         api_data['name'],
        'comments':     api_data['comments'],
        'workout_type': api_data['workout_type'],
        'class_name':   api_data['class_name'],
        'date_str':     date_str,
        'class_id':     class_id,
        'the_form':     the_form,
    }

    return render_to_response('workout_form.html', data)

def save_workout(request):
    print request.POST

    # Deal with rounds and time
    workout_type = request.POST.get('workout_type')
    if workout_type == "AMRAP":
        workout_rounds = request.POST.get('workout_reps')
        workout_time = 0
    elif workout_type == "Timed":
        workout_rounds = 0
        time_parts = request.POST.get('workout_time').split(":")
        workout_time = int(time_parts[0]) * 60 + int(time_parts[1])

    # Basic Information
    date_str = request.POST.get('date_str')
    class_id = request.POST.get('class_id')

    save_dict = {
        "time":     workout_time,
        "rounds":   workout_rounds,
        "date":     date_str,
        "class_id": class_id,

        #"variations":       [{"order": <int>, "variation_id": <int>, "element_id": <int> }, ...]
    }

    print save_dict


    return render_to_response('save_workout.html')

def no_workout_found(request, date, *args):
    return render_to_response('no_workout_found.html', {"date": date})

# =============================================================================
# = APU Endpoint ==============================================================
# =============================================================================

def json_api(request):
    """ JSON API Endpoint --
    Request  : { id: <int>, method: <string>, params: [parameters] }
    Response : { id: <int>, result: <object>, error: <object> }
    """

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

    return HttpResponse(simplejson.dumps(to_return))
