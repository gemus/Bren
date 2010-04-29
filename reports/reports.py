from crossfit.reports import date_str_to_python, get_day_of_week_str
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
