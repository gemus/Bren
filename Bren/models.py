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
        return self.completed_workout.user.username+ ", "+self.completed_workout.workout_class.workout.name+  ", "+ self.variation.name

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

    #return_dict = [{"display_name": "%s %s" % (user.first_name, user.last_name), "user_name": user.username} for user in User.objects.all()]

    return_dict = [{"user_name":"ackotia","display_name":"Ackotia Echieos"},
    {"user_name":"ashaos","display_name":"Ashaos Sigoos"},
    {"user_name":"athuos","display_name":"Athuos Jahios"},
    {"user_name":"beluos","display_name":"Beluos Kachyios"},
    {"user_name":"ceruos","display_name":"Ceruos Taiautia"},
    {"user_name":"critios","display_name":"Critios Douhios"},
    {"user_name":"croipios","display_name":"Croipios Ustotia"},
    {"user_name":"echayos","display_name":"Echayos Smuluios"},
    {"user_name":"eldeeos","display_name":"Eldeeos Onitia"},
    {"user_name":"enaos","display_name":"Enaos Clorios"},
    {"user_name":"eretia","display_name":"Eretia Sysios"},
    {"user_name":"esteeos","display_name":"Esteeos Ashatia"},
    {"user_name":"ghaoos","display_name":"Ghaoos Druxios"},
    {"user_name":"iraos","display_name":"Iraos Omios"},
    {"user_name":"jichuos","display_name":"Jichuos Weugaos"},
    {"user_name":"keipoos","display_name":"Keipoos Woraetia"},
    {"user_name":"keloitia","display_name":"Keloitia Tinitia"},
    {"user_name":"leitheos","display_name":"Leitheos Bacios"},
    {"user_name":"lylios","display_name":"Lylios Lorytia"},
    {"user_name":"moegaios","display_name":"Moegaios Linios"},
    {"user_name":"mositia","display_name":"Mositia Seretia"},
    {"user_name":"naekios","display_name":"Naekios Chrasios"},
    {"user_name":"nanoos","display_name":"Nanoos Kawuos"},
    {"user_name":"nibyos","display_name":"Nibyos Ceritia"},
    {"user_name":"nysetia","display_name":"Nysetia Palios"},
    {"user_name":"pafios","display_name":"Pafios Estutia"},
    {"user_name":"peritia","display_name":"Peritia Engatia"},
    {"user_name":"rayoitia","display_name":"Rayoitia Rodyos"},
    {"user_name":"rheluos","display_name":"Rheluos Steydios"},
    {"user_name":"rhilaios","display_name":"Rhilaios Lapios"},
    {"user_name":"rhuhyios","display_name":"Rhuhyios Rynios"},
    {"user_name":"riloos","display_name":"Riloos Eretia"},
    {"user_name":"schapios","display_name":"Schapios Nieseios"},
    {"user_name":"slarios","display_name":"Slarios Theritia"},
    {"user_name":"smaisaos","display_name":"Smaisaos Belios"},
    {"user_name":"snirtaios","display_name":"Snirtaios Vobios"},
    {"user_name":"stivios","display_name":"Stivios Lalios"},
    {"user_name":"stohios","display_name":"Stohios Sojios"},
    {"user_name":"taieatia","display_name":"Taieatia Thryhoos"},
    {"user_name":"teenaios","display_name":"Teenaios Ormytia"},
    {"user_name":"tikeos","display_name":"Tikeos Shephyios"},
    {"user_name":"tonoos","display_name":"Tonoos Onoos"},
    {"user_name":"tragios","display_name":"Tragios Quehios"},
    {"user_name":"trodeios","display_name":"Trodeios Meelios"},
    {"user_name":"turaos","display_name":"Turaos Caibyos"},
    {"user_name":"umeatia","display_name":"Umeatia Nalutia"},
    {"user_name":"uskytia","display_name":"Uskytia Voreutia"},
    {"user_name":"vesitia","display_name":"Vesitia Achios"},
    {"user_name":"vesotia","display_name":"Vesotia Denatia"},
    {"user_name":"yeicios","display_name":"Yeicios Chisios"}]

    return return_dict

    #users = User.objects.all()
    #return_dict = {
    #        "users" : users
    #        }
    #return return_dict

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

def get_workout_time(completed_workout_id):
    workout = Completed_workout.objects.get(id = completed_workout_id)
    return {"mins": workout.mins, "secs": workout.secs}


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

def get_completed_workout(workout_id, user_id):
    completed_workouts = []
    for workouts in Completed_workout.objects.filter(workout_class__workout__id__exact= workout_id, user__id__exact=user_id):
        completed_workouts.append({"workout": get_workout_name(workouts.id) , "date": get_workout_date(workouts.id), "time": get_workout_time(workouts.id)})
        for completed_element in Completed_element.objects.filter(completed_workout__id__exact=workouts.id):
            completed_workouts.append({"element": completed_element.variation.element.name , "Variation": completed_element.variation.name})

    if len(completed_workouts) > 0:
        return_dict = {
                    "completed_workouts"       : completed_workouts,
                  }
        return return_dict
    return {"error": User.objects.get(id=user_id).username + " has never done : " + Workout.objects.get(id=workout_id).name + " Before"}

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
    day = int(date[8:10])
    date = datetime.date(year,month,day)

    roster = []
    i = 0
    while i < 6 :
        roster.append({"Day": get_weekday(i)})
        for workout_class in Workout_class.objects.filter(date__exact=date).distinct():
            roster.append({"class": workout_class.class_info.title})
            for completed_workout in Completed_workout.objects.filter(workout_class__id = workout_class.id):
                roster.append({"user": completed_workout.user})
        i = i + 1
        date = datetime.date(year,month,day+i)

    return_dict = {
            "roster": roster
        }
    return return_dict

class Completed_workoutForm(forms.Form):
    mins = forms.IntegerField()
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
    co = Completed_workout()
    co.user = User.objects.get(id=create_dict['user_id'])
            #to re romoved
    co.mins = 0
            #End of remove
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
    return "Workout Saved"


def tests ():
    create_dict= {
                        "time"           : 200,
                        "rounds"         : 10,
                        "date"           : "2009-11-12",
                        "class_id"       : 1,
                        "variations"     : [{"order": 1, "variation_id" : 6,  "element_id" : 3}]

                }

    create_completed_workout(create_dict)
    return "Done"
"""
### This may need to be changed ###
    while "variation_%d" % variation_counter in request.POST:
    variation_ids.append(request.POST["variation_%d" % variation_counter])
    variation_counter += 1
    variations = [Variation.objects.get(id=x) for x in variation_ids]
    variation_counter = 0
    variation_ids = []
### End of change###
"""