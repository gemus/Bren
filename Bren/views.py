from django.shortcuts import render_to_response
from django import forms
import Crossfit.Bren.models as model

class Crazy(forms.Form):
    name = forms.CharField(max_length=20)

    def __init__(self, *args, **kw):
        super(Crazy, self).__init__(*args, **kw)
        for i in range(3):
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
    data = {
        'name':     api_data['name'],
        'comments': api_data['comments'],
    }

    return render_to_response('base.html', data)
