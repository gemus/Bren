from django.db import models
from django.contrib import admin
import datetime
from django.contrib.auth.models import User
from Crossfit.Bren.calcs import*
from django.utils import simplejson
from django import forms

DATE_FORMAT = "%Y-%m-%d"

class Workout_type(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=20)
    comments = models.CharField(max_length=200, blank = True)
    workout_type = models.ForeignKey(Workout_type)
    # TODO : Change this to a 'choices' field
    #        http://docs.djangoproject.com/en/dev/ref/models/fields/#ref-models-fields

    time = models.IntegerField()
    rounds = models.IntegerField()
    def __unicode__(self):
        return self.name

class Class_info(models.Model):
    title = models.CharField(max_length=30)
    def __unicode__(self):
        return self.title

class Workout_class(models.Model):
    date = models.DateField('Date Completed')
    workout = models.ForeignKey(Workout)
    class_info = models.ForeignKey(Class_info)
    def __unicode__(self):
        return self.workout.name+ " "+self.class_info.title + " " +self.date.isoformat()

class Completed_workout(models.Model):
    secs = models.IntegerField()
    user = models.ForeignKey(User)
    workout_class = models.ForeignKey(Workout_class)
    rounds = models.IntegerField()

    def __unicode__(self):
        return self.user.username+ ", "+ self.workout_class.workout.name

    def get_month(self):
        return get_month(self.workout_class.date.month)

    def get_weekday(self):
        return get_weekday(self.workout_class.date.weekday())

class Element(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class Element_used(models.Model):
    workout = models.ForeignKey(Workout)
    element = models.ForeignKey(Element)
    reps = models.IntegerField()
    order = models.IntegerField(null=True)
    def __unicode__(self):
        return self.workout.name+ ", "+ self.element.name

class Variation(models.Model):
    name = models.CharField(max_length=20)
    element = models.ForeignKey(Element)
    def __unicode__(self):
        return self.element.name+ ", "+ self.name

class Completed_element(models.Model):
    completed_workout = models.ForeignKey(Completed_workout)
    element_used = models.ForeignKey(Element_used)
    variation= models.ForeignKey(Variation)
    def __unicode__(self):
        return self.completed_workout.user.username+ ", "+self.completed_workout.workout_class.workout.name+  ", "+ self.variation.name + ", " + self.element_used.element.name

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

# -- API METHODS -------------- #

def get_all_users():
    """
    Returns:
    {
       "display_name": <str>,
       "user_name":     <str>,
    }
    # ordered by display_name
    """

    return [{"display_name": "%s %s" % (user.first_name, user.last_name), "user_name": user.username} for user in User.objects.all().order_by('first_name')]

def get_element(element_id):
    elm = Element.objects.get(id=element_id)
    variations = []
    for variation in Variation.objects.filter(element__id = elm.id):
        variations.append({"id": variation.id, "name": variation.name})
    element = {"id": elm.id, "name": elm.name, "variations": variations}

    return element

def get_workout_name(completed_workout_id): #Gets a workout name from a completed Workout
    workout_name = Completed_workout.objects.get(id = completed_workout_id)
    workout_name = workout_name.workout_class.workout.name
    return workout_name

def get_workout_date(completed_workout_id): #Gets a Date from a completed Workout
    workout_date = Completed_workout.objects.get(id = completed_workout_id)
    workout_date = workout_date.workout_class.date
    return workout_date.isoformat()

def _get_workout_time(completed_workout_id):
    workout = Completed_workout.objects.get(id = completed_workout_id)
    return workout.secs


def get_workout(workout_date_str, class_id):
    """
    This is where the comments would go
    """

    workout_date = datetime.datetime.strptime(workout_date_str, DATE_FORMAT).date()
    workouts = Workout_class.objects.filter(class_info__id=class_id).filter(date=workout_date)

    if len(workouts) > 0:
        workout = workouts[0].workout
        elements = []
        for elm_used in workout.element_used_set.all():
            elements.append({"reps": elm_used.reps, "element": get_element(elm_used.element.id), "order": elm_used.order})

        return_dict = {
                        "id"           : workout.id,
                        "name"         : workout.name,
                        "comments"     : workout.comments,
                        "time"         : workout.time,
                        "rounds"       : workout.rounds,
                        "workout_type" : workout.workout_type.name,
                        "elements"     : elements,
                        "class_name"   : Class_info.objects.get(pk=int(class_id)).title
                      }
        return return_dict
    return {"error": "No Class Found"}

def get_element_history(user_id, element_id):
    element_history = []
    for completed_element in Completed_element.objects.filter(completed_workout__user__id = user_id, element_used__element__id = element_id).order_by('-completed_workout__workout_class__date')[:3]:
        #year = int(completed_element.completed_workout.workout_class.date.isoformat()[:4])
        month = get_month(int (completed_element.completed_workout.workout_class.date.isoformat()[5:7]))
        day = int(completed_element.completed_workout.workout_class.date.isoformat()[8:10])
        date = str(month) + " " + str(day)# + " " + str(year)
        
        element_history.append({
                                "date"      : date,
                                "workout"   : completed_element.completed_workout.workout_class.workout.name,
                                "rounds"    : completed_element.completed_workout.workout_class.workout.rounds,
                                "reps"      : completed_element.element_used.reps,
                                "variation" : completed_element.variation.name,
        })  

    if len(element_history) > 0:
        return element_history 
    return {"error": "You has never recorded " + Element.objects.get(id = element_id).name + " Before"}

def get_workout_element_history(user_id, workout_id):
    workout_element_history = []
    for element in Element_used.objects.filter(workout__id = workout_id):
        workout_element_history.append({
                                        "element" : element.element.name,
                                        "history" : get_element_history(user_id, element.element.id),
        })
    return workout_element_history
        

def get_last_attended_class(user_id):
    for cwo in Completed_workout.objects.filter(user__id__exact=user_id).order_by('-workout_class__date')[:1]:
        last_class = cwo.workout_class.class_info
        return {'id': last_class.id, 'title': last_class.title}
    return None

def get_completed_workout(user_id, workout_id):
    completed_workouts = []
    for workouts in Completed_workout.objects.filter(workout_class__workout__id__exact= workout_id, user__id__exact=user_id).order_by('workout_class__date'):
        workout = {
            'id' : workouts.id,
            'workout' : get_workout_name(workouts.id),
            'date': get_workout_date(workouts.id),
            }

        type_name = Workout.objects.get(id=workout_id).workout_type.name
        if type_name == "Timed":
            type_value = {"type" : "Timed", "time": workouts.secs}
        elif type_name == "AMRAP":
            type_value = {"type" : "AMRAP", "time": workouts.rounds}
        else:
            type_value = {"type" : "Done"}
        workout.update({"info": type_value})
        
        variations = []    
        for completed_element in Completed_element.objects.filter(completed_workout__id__exact=workouts.id).order_by('element_used__order'):
            variations.append({"element": completed_element.variation.element.name , "variation": completed_element.variation.name})

        workout.update({"variations" : variations})
        completed_workouts.append(workout)

    return completed_workouts

def get_classes(date):      #Expecting string comming in as "YYYY-MM-DD"
    year = int(date[:4])                    #Formating the incomming string
    month = int(date[5:7])
    day = int(date[8:10])
    date = datetime.date(year, month, day)
    workout_class_list = []

    for classes in Workout_class.objects.filter(date__exact=date):
        workout_class_list.append ({"name": classes.class_info.title , "id": classes.class_info.id})

    return_dict = {
            "workout_class_list": workout_class_list,
        }
    return return_dict

def get_week_roster(date):      #Expecting string comming in as SUNDAY! as "YYYY-MM-DD"

    year = int(date[:4])                    #Formating the incomming string
    month = int(date[5:7])
    dday = int(date[8:10])
    date = datetime.date(year,month,dday)

    while not date.weekday() == 6:
        dday = dday - 1
        date = datetime.date(year,month,dday)
    days = []
    i = 0
    while i < 6:
        days.append ({"day": get_weekday(i), "classes": []})
        i = i + 1
    for day in days:
        classes = []
        for workout_class in Workout_class.objects.filter(date = date):
            users = []
            for co in Completed_workout.objects.filter(workout_class__id = workout_class.id):
                users.append({"user" : co.user.first_name})
            classes.append({"class_name" : workout_class.class_info.title, "users" : users, "class_id" : workout_class.id})
        dday = dday + 1
        date = datetime.date(year,month,dday)
        day['classes'] = classes
    return days

class Completed_workoutForm(forms.Form):
    secs = forms.IntegerField()
    rounds = forms.IntegerField()

def create_completed_workout(create_dict):
    """expects dictionary like
    {
        "user_id":          <int>,
        "time":             <int>,  (time in seconds)
        "rounds":           <int>,

        "date":             <str>,  (format: yyyy/mm/dd)
        "class_id":         <int>,

        "variations":       [{"order": <int>, "variation_id": <int>, "element_id": <int> }, ...]
    }
    """

    date = datetime.datetime.strptime(create_dict['date'], DATE_FORMAT).date()
    workout_class_id = Workout_class.objects.filter(date=date).get(class_info__id = create_dict['class_id']).id

    if len( Completed_workout.objects.filter(user__id =create_dict['user_id'], workout_class__id = workout_class_id)) == 0:
        co = Completed_workout()
    else :
        co = Completed_workout.objects.filter(user__id =create_dict['user_id']).get(workout_class__id = workout_class_id)
        for completed_element in Completed_element.objects.filter(completed_workout__id = co.id):
            completed_element.delete()

    co.user = User.objects.get(id=create_dict['user_id'])
    co.date = date
    co.secs = create_dict['time']
    co.rounds = create_dict['rounds']
    workout_class_id = Workout_class.objects.filter(date=date).get(class_info__id = create_dict['class_id']).id
    co.workout_class = Workout_class.objects.get(id=workout_class_id)
    co.save()
    workout = Workout_class.objects.get(id=workout_class_id).workout
    for variation in create_dict['variations']:
        ce = Completed_element()
        ce.completed_workout = co
        ce.variation = Variation.objects.get(id = variation['variation_id'])
        ce.element_used = Element_used.objects.filter(workout__id = workout.id).get(order = variation['order'])
        ce.save()
