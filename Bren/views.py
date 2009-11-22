from django.shortcuts import render_to_response
from django import forms
import Crossfit.Bren.models as model

class WorkoutForm(forms.Form):
    date = forms.DateField()

    def __init__(self, elements, *args, **kw):
        super(WorkoutForm, self).__init__(*args, **kw)
        for i, field_dict in enumerate(elements):
            field = forms.ChoiceField()
            field.choices = [ (varient['id'], varient['name']) for varient in field_dict['element']['variations']]

            field.label = "%d %s" % (field_dict['reps'], field_dict['element']['name'])
            self.fields['extra_info_%d' % i] = field

def workout_form(request):
    api_data = model.get_workout(1, 1)
    the_form = WorkoutForm(api_data['elements'])

    data = {
        'name':         api_data['name'],
        'comments':     api_data['comments'],
        'workout_type': api_data['workout_type'],
        'the_form':     the_form,
    }

    return render_to_response('workout_form.html', data)

def index(request):
    return render_to_response('index.html')