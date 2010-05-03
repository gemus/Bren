from crossfit.reports import date_str_to_python, get_day_of_week_str, python_date_to_display_str
from crossfit.bren.models import *

"""
=== Design Philosophy =========================================================
Each report is heavily tied to the queries and the model. So it seems quite
excessive to create model calls for these reports. The exception is if we put
a lot of time into the bren model API so these reports could be created from
those API calls. This would be an ideal situation, but for now it will have to
wait.
"""

def completed_workouts(start_date, end_date, user):
    """
    Given a start and end date, will generate a dictionary that can be fed into
    the completed_workouts template for direct display or sending via email
    """

    the_workouts = []
    for i in Completed_workout.objects.filter(user=user)\
                .filter(workout_class__date__range=(start_date, end_date))\
                .order_by("workout_class__date"):
        workout_info = get_completed_workout_info(i.id)

        # Make a user friendly version of the date
        workout_date = date_str_to_python(workout_info['date'])
        workout_info['date_display'] = get_day_of_week_str(workout_date)

        # Create a user friendly version of the time
        if 'time' in workout_info['info']:
            time_val = workout_info['info']['time']
            minutes = time_val / 60
            seconds = time_val % 60
            time_display = "%d:%d" % (minutes, seconds)
            workout_info['info']['time_display'] = time_display

        the_workouts.append(workout_info)

    display_name = "%s" % (user.first_name)

    if display_name[-1:] == 's':
        display_name += "'"
    else:
        display_name += "'s"
        
    return {'workouts': the_workouts, 'display_name': display_name}


def attendence(start_date, end_date, user):
    """
    Given a start and end date, will generate the attendence for the time period
    """
    start_date = date_str_to_python(start_date)
    end_date = date_str_to_python(end_date)
    datedelta = datetime.timedelta(days=1)
    date = start_date
    attendence = []
    
    while date != end_date + datedelta:
        attendence.append ({
            'date': date,
            'workout_classes' : []
        })
        date = date + datedelta
        
    for day in attendence:
        workout_classes = []
        for workout_class in Workout_class.objects.filter(date = day['date']):
            users = []
            for co in Completed_workout.objects.filter(workout_class__id = workout_class.id):
                users.append (co.user.first_name)
            user_number = len(users)
            
            day['workout_classes'].append({
                'class_name' : workout_class.class_info.title,
                'users': users,
                'user_number' : user_number,
                })
                
    for date in attendence:
        date['date'] = python_date_to_display_str(date['date'])
           
    return_data = {
        'start_date' : python_date_to_display_str(start_date),
        'end_date' : python_date_to_display_str(end_date),
        'attendence' : attendence
        }
    return return_data

def ranking(workout_id, date):
    """
    Purpose : Given a workout ID and date rank users
    Params:
        "workout.id" : ID of the workout we are ranking (INT)
        "date" : The date of the workout in YYYY-MM-DD format (STRING)
    Returns:
        "workout_name" : The name of the workout(STRING)
        "workout_ranking": A list or the completed workouts in order(LIST)
    """
    workout_ranking = []
    date = datetime.datetime.strptime(date, DATE_FORMAT)
    workout = Workout.objects.get(id=workout_id)    
    workout_elements = Element_used.objects.filter(workout__id = workout_id)  
    if  workout.workout_type == 'Timed': order_by = "secs"
    elif  workout.workout_type == 'AMRAP': order_by = "-rounds"
    elif  workout.workout_type == 'Done': order_by = "user__first_name"
    completed_workouts = Completed_workout.objects.filter(workout_class__workout__id = workout_id, workout_class__date = date).order_by(order_by)
    for co in completed_workouts:
        workout_ranking.append(get_completed_workout_info(co.id))
    if  workout.workout_type == 'Timed' :
        for co in workout_ranking:
            mins = co['info']['time'] / 60
            secs = co['info']['time'] % 60
            co['info']['time'] = "%d:%02d" % (mins, secs)
    return_data = {
    "workout_name" : workout.name,
    "workout_elements": workout_elements,
    "workout_type" : workout.workout_type,
    "workout_date" : python_date_to_display_str(date),
    "workout_ranking" : workout_ranking,
    }
    
    return return_data
 