import datetime

from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from crossfit.bren.models import *

"""
=== Design Philosophy =========================================================
Each view is a report, and heavily tied to the queries. So no point in
separating out the model calls into its own module. Each view will define its
own set of queries to be sent directly to the template.

If there is a lot of code reuse that we can do from the reports (which I
currently doubt), then it will make sense to separate them into their own
module.
"""

DATE_FORMAT = "%Y-%m-%d"
def date_str_to_python(date_str):
    return datetime.datetime.strptime(date_str, DATE_FORMAT)

# Instead of getting a user_id get a User object as the 2nd param
def report_user(func):
    def new_func(*args, **kw):
        user = User.objects.get(pk=int(args[1]))
        return func(args[0], user, *args[2:], **kw)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func

def index(request):
    return render_to_response('reports/index.html')

@report_user
def completed_workouts(request, user):
    """
    Given a start and end date, will display all completed workouts for the given user.
    Will also show progression where it can.
    """

    start_date = date_str_to_python(request.GET['start_date'])
    end_date = date_str_to_python(request.GET['end_date'])

    for i in Completed_workout.objects.filter(user=user).filter(workout_class__date__range=(start_date, end_date)):
        print get_completed_workout_info(i.id)


    return render_to_response('reports/completed_workouts.html')