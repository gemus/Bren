from django.db import models
from django.contrib import admin
import datetime
from django.contrib.auth.models import User
from Crossfit.Bren.calcs import*
from django.utils import simplejson

class Workout_type(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=20)
    comments = models.CharField(max_length=200)
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
    mins = models.IntegerField()
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
    def __unicode__(self):
        return self.workout.name+ ", "+ self.element.name

class Variation(models.Model):
    name = models.CharField(max_length=20)
    element = models.ForeignKey(Element)
    def __unicode__(self):
        return self.element.name+ ", "+ self.name

class Variation_used(models.Model):
    completed_workout= models.ForeignKey(Completed_workout)
    variation= models.ForeignKey(Variation)
    def __unicode__(self):
        return self.completed_workout.user.username+ ", "+self.completed_workout.workout_class.workout.name+  ", "+ self.variation.name

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)


# -- API METHODS -------------- #
def get_element(element_id):
    elm = Element.objects.get(id=element_id)
    return {"id": elm.id, "name": elm.name}

def get_workout_name(completed_workout_id):
    workout_name = Completed_workout.objects.get(id = completed_workout_id)
    workout_name = workout_name.workout_class.workout.name
    return {"id": completed_workout_id, "name": workout_name}


def get_workout(workout_date, class_id):
    workout = Workout.objects.get(id=1)

    elements = []
    for elm_used in workout.element_used_set.all():
        elements.append({"reps": elm_used.reps, "element": get_element(elm_used.element.id)})

    return_dict = {
                    "id"       : workout.id,
                    "name"     : workout.name,
                    "comments" : workout.comments,
                    "time"     : workout.time,
                    "rounds"   : workout.rounds,
                    "type"     : workout.workout_type.name,
                    "elements" : elements,
                  }

    return return_dict

def get_completed_workout(workout_id, user_id):
    workout = get_workout_name(28)
    completed_workouts = []
    for workouts in Completed_workout.objects.filter(workout_class__workout__id__exact= 1):#, user__id__exact=user_id)
        completed_workouts.append({"workout": workouts.workout_class.workout.name , "date": workouts.workout_class.date.isoformat()})

    return_dict = {
                    "completed_workouts"       : completed_workouts,
                  }

    return return_dict

def create_completed_workout(create_dict):
    """expects dictionary like
    {
        "user_id":          <int>,
        "date_of_class":    <int>,
        "class_name":       <string>,

        "mins":             <int>,
        "sec":              <int>,
        "rounds":           <int>,
        "variations":       [{stuff}, {more stuff}],
    }
    """
    pass
