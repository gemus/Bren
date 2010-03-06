import datetime

from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from crossfit.bren.models import *
from crossfit.email_sender.sender import email_user

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

OUTPUT_FORMAT = "%A %B %d, %Y" # December 1, 2009
def python_date_to_display_str(python_date):
    return python_date.strftime(OUTPUT_FORMAT).replace(' 0', ' ')

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

    the_workouts = []
    for i in Completed_workout.objects.filter(user=user)\
                .filter(workout_class__date__range=(start_date, end_date))\
                .order_by("workout_class__date"):
        workout_info = get_completed_workout_info(i.id)

        # Make a user friendly version of the date
        workout_date = date_str_to_python(workout_info['date'])
        workout_info['date_display'] = python_date_to_display_str(workout_date)

        # Create a user friendly version of the time
        if 'time' in workout_info['info']:
            time_val = workout_info['info']['time']
            minutes = time_val / 60
            seconds = time_val % 60
            time_display = "%d:%d" % (minutes, seconds)
            workout_info['info']['time_display'] = time_display

        the_workouts.append(workout_info)

    email_user(user, 'Email Subject', 'reports/completed_workouts.html', {'workouts': the_workouts})

    return render_to_response('reports/completed_workouts.html', {'workouts': the_workouts})