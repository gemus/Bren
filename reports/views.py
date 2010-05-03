from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from crossfit.bren.models import *
from crossfit.reports import reports
from crossfit.reports import date_str_to_python

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

    data = reports.completed_workouts(start_date, end_date, user)

    return render_to_response('reports/completed_workouts.html', data)

def attendence(request, user):
    """
    Given a start and end date, will generate the attendence for the time period
    """
    start_date = "2010-1-4"
    end_date = "2010-1-15"
    
    #start_date = date_str_to_python(request.GET['start_date'])
    #end_date = date_str_to_python(request.GET['end_date'])

    data = reports.attendence(start_date, end_date, user)

    return render_to_response('reports/attendence.html', data)

def ranking(request, user):
    """
    Given a start and end date, will generate the attendence for the time period
    """
    date = "2010-01-29"
    workout_id = "10"
    #workout_id = request.GET['workout_id']
    #date = date_str_to_python(request.GET['end_date'])
    data = reports.ranking(workout_id, date)
    return render_to_response('reports/rankings.html', data)