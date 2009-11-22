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
    date = forms.DateField()

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
        'the_form':     the_form,
    }

    return render_to_response('workout_form.html', data)

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
