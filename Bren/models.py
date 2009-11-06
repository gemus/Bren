from django.db import models
from django.contrib import admin
import datetime
from django.contrib.auth.models import User
from Crossfit.Bren.calcs import*


class Workout_type(models.Model):
    name = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=20)
    comments = models.CharField(max_length=200)
    workout_type = models.ForeignKey(Workout_type)
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
def get_workout(workout_date, class_id):
    return "some fancy JSON stuff"
