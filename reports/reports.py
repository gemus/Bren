from crossfit.reports import *
from crossfit.bren.models import *
from crossfit.email_sender.models import*
from django.conf import settings

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
            time_display = "%d:%02d" % (minutes, seconds)
            workout_info['info']['time_display'] = time_display

        the_workouts.append ({
            'workout_info'      : workout_info,
            'workout_rounds'    : i.workout_class.workout.rounds,
            'workout_time'      : i.workout_class.workout.time,
            })

    display_name = "%s" % (user.first_name)

    if display_name[-1:] == 's':
        display_name += "'"
    else:
        display_name += "'s"
    try:
        unsubscribe_hash = UserEmailPermissions.objects.get(user=user).subscribe_hash
        unsubscribe_url = "%semail/unsubscribe/%s/" % (settings.CONFIRM_EMAIL_PERM_BASE_URL,
                                                       unsubscribe_hash)
    except UserEmailPermissions.DoesNotExist:
        unsubscribe_url = '#'

    return {'workouts'        : the_workouts,
            'display_name'    : display_name,
            'unsubscribe_url' : unsubscribe_url,
            'start_date'      : python_date_to_short_display_str(start_date),
            'end_date'        : python_date_to_short_display_str(end_date)
            }

def attendance(start_date, end_date):
    """
    Given a start and end date, will generate the attendance for the time period
    """
    datedelta = datetime.timedelta(days=1)
    date = start_date
    attendance = []
    number_of_days = (end_date - start_date).days
    while number_of_days >= 0:
        number_of_days = number_of_days - 1
        attendance.append ({
            'date': date,
            'workout_classes' : []
        })
        date = date + datedelta
    user_count = {}
    for day in attendance:
        workout_classes = []
        for workout_class in Workout_class.objects.filter(date = day['date']):
            users = []
            for co in Completed_workout.objects.filter(workout_class__id = workout_class.id):
                users.append (co.user.first_name)
                name_key = co.user.first_name + " " + co.user.last_name
                if not name_key in user_count :
                    user_count.update({ name_key : 1})
                else:
                    user_count[name_key] = user_count[name_key] + 1
            user_number = len(users)

            day['workout_classes'].append({
                'class_name' : workout_class.class_info.title,
                'users': users,
                'user_number' : user_number,
                })
    users_attendance = []
    for key in  user_count.keys():
        users_attendance.append({'name': key, 'num': user_count[key]})
    users_attendance.sort()
    for date in attendance:
        date['date'] = python_date_to_display_str(date['date'])
    return_data = {
        'start_date' : python_date_to_display_str(start_date),
        'end_date' : python_date_to_display_str(end_date),
        'attendance' : attendance,
        'users_attendance' : users_attendance,
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
    workout = Workout.objects.get(id=workout_id)
    workout_elements = Element_used.objects.filter(workout__id = workout_id).order_by('order')
    if  workout.workout_type == 'Timed': order_by = "secs"
    elif  workout.workout_type == 'AMRAP': order_by = "-rounds"
    elif  workout.workout_type == 'Done': order_by = "user__first_name"
    completed_workouts = Completed_workout.objects.filter(workout_class__workout__id = workout_id, workout_class__date = date).order_by(order_by)
    for co in completed_workouts:
        workout_ranking.append(get_completed_workout_info(co.id))

    total = 0
    number = 0
    for co in completed_workouts:
        number = number + 1
        if  workout.workout_type == 'Timed': total = total + co.secs
        elif  workout.workout_type == 'AMRAP': total = total + co.rounds
    if not number == 0:
        workout_average = total / number
    elif number == 0:
        workout_average = 0

    for co in workout_ranking:
        if workout.workout_type == 'Timed':
            plus_minus = co['info']['time'] - workout_average

            if plus_minus < 0: mins = plus_minus // 60 + 1
            elif plus_minus >= 0: mins = plus_minus // 60

            if plus_minus < 0: secs = 60 - (plus_minus % 60)
            elif plus_minus >= 0: secs = plus_minus % 60

            plus_minus = "%d:%02d" % (mins, secs)

        if workout.workout_type == 'AMRAP': plus_minus = co['info']['rounds'] - workout_average

        try:
            co.update({"plus_minus": plus_minus})
        except NameError:
            continue

    if  workout.workout_type == 'Timed' :
        mins = workout_average / 60
        secs = workout_average % 60
        workout_average = "%d:%02d" % (mins, secs)

        for co in workout_ranking:
            mins = co['info']['time'] / 60
            secs = co['info']['time'] % 60
            co['info']['time'] = "%d:%02d" % (mins, secs)

    workout_info = {
        "name"          :workout.name,
        "elements"      :workout_elements,
        "comments"      :workout.comments,
        "rounds"        :workout.rounds,
        "time"          :workout.time,
        }

    return_data = {
    "workout_info" : workout_info,
    "workout_type" : workout.workout_type,
    "workout_date" : python_date_to_display_str(date),
    "workout_ranking" : workout_ranking,
    "workout_average" : workout_average,
    }

    return return_data

def class_brakedown(start_date, end_date):
    datedelta = datetime.timedelta(days=1)
    date = start_date
    workout_classes = {}
    number_of_days = (end_date - start_date).days

    while number_of_days >= 0:

        day = get_day_of_week_str(date)

        for workout_class in Workout_class.objects.filter(date = date):
            user_number = 0
            date_class = day + " " + workout_class.class_info.title

            if not date_class in workout_classes:
                workout_classes.update({
                    date_class :  Completed_workout.objects.filter(workout_class = workout_class).count()
                    })

            elif date_class in workout_classes:
                workout_classes[date_class] = workout_classes[date_class] + Completed_workout.objects.filter(workout_class = workout_class).count()


        number_of_days = number_of_days - 1
        date = date + datedelta

    class_numbers = []
    for key in workout_classes.keys():
        class_numbers.append({
        'name': key,
        'num': workout_classes[key],
        })

    class_numbers.sort()
    for classes in class_numbers :
        print classes

