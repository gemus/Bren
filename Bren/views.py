from django.shortcuts import render_to_response
from django import forms
import Crossfit.Bren.models as model

class WorkoutForm(forms.Form):
    name = forms.CharField(max_length=20)

    def __init__(self, elements, *args, **kw):
        super(WorkoutForm, self).__init__(*args, **kw)
        for i, field_dict in enumerate(elements):
            self.fields['extra_info_%d' % i] = forms.CharField(max_length=20)

def index(request):
    #{
    #'id': 1,
    #'name': u'Fran',
    #'comments': u'a',
    #'time': 12,
    #'type': u'Timed',
    #'rounds': 12,
    #
    #'elements': [   {'reps': 15, 'element': {'id': 3, 'name': u'Pull Up'}},
    #                {'reps': 15, 'element': {'id': 4, 'name': u'Thursters'}}
    #            ],
    #
    #}

    api_data = model.get_workout(1, 1)
    the_form = WorkoutForm(api_data['elements'])
    data = {
        'name':     api_data['name'],
        'comments': api_data['comments'],
        'the_form': the_form,
    }

    print api_data

    return render_to_response('base.html', data)
