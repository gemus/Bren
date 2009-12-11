from django.db import models
from django.contrib import admin
import datetime
from django.contrib.auth.models import User
from Crossfit.Bren.calcs import*
from django.utils import simplejson

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
def get_user_info(user_id):
    user = User.objects.get(id =user_id)
    user_dict = {
        "username"      : user.username,
        "first_name"    : user.first_name,
        "last_name"     : user.last_name,
        "email"         : user.email,
        "pin"           : 11111,
        "pin_again"     : 11111,
        }
    return user_dict

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
    """
    Purpose: Given a element id output element and all its variation
    Input: element_id (INT)
    Output:
            "id"        : The id of the element (INT)
            "name"      : The name of the element (STRING)
            "variations : A list of variation dictionarys contaiting(LIST)
                          "id" : The of the variation(INT)
                          "name" : The name of the variation(STRING)
    """
    elm = Element.objects.get(id=element_id)
    variations = []
    for variation in Variation.objects.filter(element__id = elm.id):
        variations.append({"id": variation.id, "name": variation.name})
    element = {"id": elm.id, "name": elm.name, "variations": variations}
    return element

def get_workout(workout_date_str, class_id):
    """
    Purpose: Given a workout date and class return the workout data
    Input: 
        workout_date_str : The date of the workout in YYYY-MM-DD format (STRING)
        class_id : the class id (INT)

    Output:
        "id"           : The workout id (INT)
        "name"         : The workout name (STRING)
        "comments"     : The workout comment (STRING)
        "time"         : The time allowed for a AMRAP workout(INT)
        "rounds"       : The number of rounds for the workout(INT)
        "workout_type" : The type of workout AMRAP, TIMES, DONE ect.
        "elements"     : A list of all the elements in a workout
                         "id"           : element id,
                         "name"         : element name,
                         "variations"   : A list of variations
                                          "id" : variation id
                                          "name" : variation name}}(LIST)
        "class_name"   : The name of the workout class(STRING)
        "workout_class": The id of the workout class(INT)
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
                        "class_name"   : Class_info.objects.get(pk=int(class_id)).title,
                        "workout_class": workouts[0].id,
                      }
        return return_dict
    return {"error": "No Class Found"}

def get_element_history(user_id, element_id):
    """
    Purpose: Given a user and element return the users history with the element in list form
    Input:
            user_id : user's id as (INT)
    Output:
            A List of       : Times the user has done the element
            
            "workout"       : The name of the workout the each element is coming from(STRING)
            "rounds"        : How many round of reps for the element(INT)
            "reps"          : How many reps per round of the element(INT)
            "variation"     : The name of the variation on the element(STRING) 
            "variationn_id" : The id of the variation (INT)
    Or Output:
            "Error"         : you have never done the element before(STRING)
    """

    element_history = []
    for completed_element in Completed_element.objects.filter(completed_workout__user__id = user_id, element_used__element__id = element_id).order_by('-completed_workout__workout_class__date')[:3]:        
        element_history.append({
                                "workout"       : completed_element.completed_workout.workout_class.workout.name,
                                "rounds"        : completed_element.completed_workout.workout_class.workout.rounds,
                                "reps"          : completed_element.element_used.reps,
                                "variation"     : completed_element.variation.name,
                                "variationn_id" : completed_element.variation.id,
        })  

    if len(element_history) > 0:
        return element_history 
    return {"error": "You has never recorded " + Element.objects.get(id = element_id).name + " Before"}

def get_workout_element_history(user_id, workout_id):
    """
    Purpose: Given a user and a workout output the element history of all the elements in the workout
    Input:
            user_id     : The users id (INT)
            workout_id  : The workouts id (INT)
    Output:
            A List of           : The  elements that happend in the workout
            
            "element"           : The name of the element(STRING)
            "element_id"        : The id of the element(INT)
            "history"           : The history of that element (LIST) (See get_element_history for details)
            "last_variation"    : What the user did the last he did the element (DICT) (See get_element_history for details)   
    """

    workout_element_history = []
    element_list = {}
    for element in Element_used.objects.filter(workout__id = workout_id):
        history = get_element_history(user_id, element.element.id)
        if not 'error' in history:
            last_variation = history[0]['variation']
        else:
            last_variation = "No record"
        
        
        if not element.element.id in element_list:
            element_list.update({element.element.id : 1})
            workout_element_history.append({
                                        "element"           : element.element.name,
                                        "element_id"        : element.element.id,
                                        "history"           : history,
                                        "last_variation"    : last_variation, 
                                      })
    return workout_element_history
        

def get_last_attended_class(user_id):
    """
    Purpose: Given a user return the last class the attended
    Input: user_id     : The users id (INT)
    Output:
            "id"        : The id of the last class(INT)
            "title"     : The title of the class(STRING)
    """
    for cwo in Completed_workout.objects.filter(user__id__exact=user_id).order_by('-workout_class__date')[:1]:
        last_class = cwo.workout_class.class_info
        return {'id': last_class.id, 'title': last_class.title}
    return None


def get_completed_workout(user_id, workout_id):
    """
    Purpose: Given a user and a workout return times the user has done the workout
    Input:
            user_id     : The users id (INT)
            workout_id  : The workout id (INT)
    Output:
            A List of   : Times the user has done the workout
            
            "id"        : The id of the completed workout(INT)
            "workout"   : The name of the workout(STRING)
            "date"      : The date they did the workout in YYYY-MM-DD format(STRING)
            "info"      : The information about type of workout and score based on that {"info": type_value} (DICT)
                        : type_value if Timed equals {"type" : "Timed", "time": the amount of time it took in secs(INT)}
                        : type_value if AMRAP equals {"type" : "AMRAP", "rounds": how many rounds the user did(INT)}
                        : type_value if Done equals  {"type" : "Done"}
         "variations"   : a list of the variations that the user inputed as ("element" : The name of the element(STRING), "variation" : the name of the variation used(STRING)}
            
    """                 
    completed_workouts = []
    for workouts in Completed_workout.objects.filter(workout_class__workout__id__exact= workout_id, user__id__exact=user_id).order_by('workout_class__date'):
        workout = {
            'id' : workouts.id,
            'workout' : workouts.workout_class.workout.name,
            'date': workouts.workout_class.date.isoformat(),
            }
        type_name = Workout.objects.get(id=workout_id).workout_type.name
        if type_name == "Timed":
            type_value = {"type" : "Timed", "time": workouts.secs}
        elif type_name == "AMRAP":
            type_value = {"type" : "AMRAP", "rounds": workouts.rounds}
        else:
            type_value = {"type" : "Done"}
        workout.update({"info": type_value})
        variations = []    
        for completed_element in Completed_element.objects.filter(completed_workout__id__exact=workouts.id).order_by('element_used__order'):
            variations.append({"element": completed_element.variation.element.name , "variation": completed_element.variation.name})
        workout.update({"variations" : variations})
        completed_workouts.append(workout)
    return completed_workouts

def get_classes(date):
    """
    Purpose: Given a date output what classes happend
    Input:
            date     : The date in YYYY-MM-DD format (STRING)
    Output:
            A list of   : Classes that happend that day
            "name"      : The name of the class(STRING)
            "id"        : The id of the class
    """  
    date = datetime.datetime.strptime(date, DATE_FORMAT)
    workout_class_list = []
    for classes in Workout_class.objects.filter(date__exact=date):
        workout_class_list.append ({"name": classes.class_info.title , "id": classes.class_info.id})
    return_dict = {
            "workout_class_list": workout_class_list,
        }
    return return_dict

def get_week_roster(date):
    """
    Purpose: Given a date output the weeks classes each day and the people that did them.
    Input:
            date     : The date in YYYY-MM-DD format (STRING)
    Output:
            A list of   : Days of the week
            "daye"      : Name of the day of the ect. "Sunday" (STRING)
            "classes"   : A list of the classes that happend that day
                        : {"class_name" : the name of the class(STRING), "class_id" : the class id of the class(INT),  "user" : a list of the users (LIST) as {"user" : The users first name}  
    """ 
    date = datetime.datetime.strptime(date, DATE_FORMAT)
    datedelta = datetime.timedelta(days=1)
    while not date.weekday() == 6:
        date = date - datedelta
    days = []
    i = 0
    while i <= 6:
        days.append ({"day": get_weekday(i), "classes": []})
        i = i + 1
    for day in days:
        classes = []
        for workout_class in Workout_class.objects.filter(date = date):
            users = []
            user_number = 0
            for co in Completed_workout.objects.filter(workout_class__id = workout_class.id):
                users.append({"user" : co.user.first_name})
                user_number = user_number + 1
            classes.append({"class_name" : workout_class.class_info.title, "users" : users, "class_id" : workout_class.id, "user_number" : user_number,})
        date = date + datedelta
        day['classes'] = classes
    return days

def create_completed_workout(create_dict):
    """
    Purpose: Given a dictionary of a workout to be saved, save it
    Input:
        "user_id"   : The id of the user that did the workout(INT),
        "time"      : The amount of time the workout took if its Timed in seconds(INT)
        "rounds"    : The rounds of the workout the user did if its AMRAP(INT),
        "date"      : The date of the workout in YYYY-MM-DD format (STRING)
        "class_id"  : The workout class id (INT)
        "variations": A list of the variations of the workout as
                      "order"       : what spot in order of the workout the element is in (INT),
                      "variation_id": The id of the variation(INT),
                      "element_id"  : the id of the element(INT)}

    Output:
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

def create_user(user_dict):
    """
    Purpose: Given a dictionary of a user add the user to the database
    Input:
        "username"      : The id of the user that did the workout(INT),
        "first_name"    : The amount of time the workout took if its Timed in seconds(INT)
        "rounds"        : The rounds of the workout the user did if its AMRAP(INT),
        "last_name"     : The date of the workout in YYYY-MM-DD format (STRING)
        "pin"           : The pin the user entered (INT)
        "pin_again"     : The pin to confirm the entry (INT)
        "email"         : The users e-mail address(EMAIL) (OPTIONAL)
        
    Output:
    """

    if not user_dict['pin'] == user_dict['pin_again']:
        return {"pin_error": "PIN and PIN again did not match"}
    if not User.objects.filter(username = user_dict['username']).count() == 0:
        return { "username_error" : "User name is already taken"}
    user = User()
    user.username = user_dict['username']
    user.first_name = user_dict['first_name']
    user.last_name = user_dict['last_name']
    user.set_password(user_dict['pin'])
    if 'email' in user_dict:
        user.email = user_dict['email']
    user.save()

def user_done_class(user_id, workout_class_id):
    """
    Purpose: Given a user and workout class return the completed workout if they have done it
    Input:
        "user_id"               : The id of the user(INT),
        "workout_class_id"      : The id of the workout class(INT)        
    Output: The completed workout or None if they haven't done it
    """
    done = Completed_workout.objects.filter(user__id = user_id, workout_class__id = workout_class_id)
    if not len(done) == 0:
        return done[0]
    else:
        return None

def get_workout_variations(user_id, workout_class_id):
    """
    Purpose: Given a user id and workout class id create a dictionary that will set the variations
    Input:
        "user_id"               : The id of the user(INT),
        "workout_class_id"      : The id of the workout class(INT)
        
    Output:
        A dictionary of
        elements of the workouts form style      The variation that they previously selected of saved
        "varient_ element.id_elements.order"    : variation.id(INT)
    """
    days_workout = Completed_workout.objects.filter(user__id = user_id, workout_class__id = workout_class_id)
    if not len(days_workout) == 0:
        return get_previous_variations(days_workout[0].id)
    else:
        workout_id = Workout_class.objects.get(id = workout_class_id).workout.id
        previous_workouts = Completed_workout.objects.filter(workout_class__workout__id = workout_id, user__id = user_id).order_by('-workout_class__date')
        if not len(previous_workouts) == 0:
            return get_previous_variations(previous_workouts[0].id)
        else:
            return get_workout_estimation(user_id, workout_id)

    
def get_previous_variations(completed_workout_id):
    """
    Purpose: Given a completed workout output the variations used
    Input:
        "completed_workout_id"  : The id of the completed workout(INT),
    Output:
        A dictionary of
        elements of the workouts form style      The variation that they been saved
        "varient_ element.id_elements.order"    : variation.id
    """
    return_dict = {}
    completed_elements = Completed_element.objects.filter(completed_workout__id=completed_workout_id)
    for variation in completed_elements:
        element = "varient_" + str(variation.element_used.element.id)+ "_"+ str(variation.element_used.order)
        variation_id = variation.variation.id
        return_dict.update ({ element : variation_id })
    return return_dict
    
def get_workout_estimation(user_id, workout_id):
    """
    Purpose: Given a user and workout select the variation for the form to the last variations they used on each element
    Input:
        "user_id"       : The id of the user(INT),
        "workout_id"    : The id of the workout(INT)
    Output:
        A dictionary of
        elements of the workouts form style      The variation that they been saved
        "varient_ element.id_elements.order"    : variation.id
    """
    return_dict = {}
    elements_used = Element_used.objects.filter(workout__id = workout_id)
    for elements in elements_used:
        element_history = get_element_history(user_id, elements.element.id) 
        if not 'error' in element_history:
            element = "varient_" + str(elements.element.id)+ "_" + str(elements.order)
            variation_id = element_history[0]['variationn_id']
        else:
            element = "varient_" + str(elements.element.id)+ "_" + str(elements.order)
            variation_id = Variation.objects.filter(element__id = elements.element.id)[0].id
        return_dict.update ({ element : variation_id })
    return return_dict

def get_full_element_history(user_id, element_id):
    """
    Purpose: Given a user and element return the full history that user has done on that element
    Input:
        "user_id"       : The id of the user(INT),
        "element_id"    : The id of the element(INT)
    Output:
        A dictionary of:
        'user_name'         : The first name of the user (STRING)
        'element_name'      : The name of the element (STRING)
        'total'             : The number of totaly times the user has done that element (INT)
        'element_history'   : A list of variations to that element(LIST)
                            : "variation name" : The name of the variation (STRING), "variation_history" : A list of times that variation was done(LIST)
                            : "variation_history": A list of times a variation was done
                                                   "date"    : The date the variaition was done in YYYY-MM-DD format(STRING)}
                                                   "reps"    : How many were done(INT)
                                                   "rounds"  : How many rounds(INT)
                            : "first"  : A dictionary about the first time a variation was done
                                         "date"     : The date it was first done im YYYY-MM-DD format
                                         "workout"  : The name of the workout it was first done in
                                         "reps"     : How many reps for the first time
                                         "rounds"   : How many rounds the first time                                                    
    """
    total = 0
    element = Element.objects.get(id = element_id)
    variations = Variation.objects.filter(element__id = element_id)
    element_history = []
    for variation in variations:
        count = 0
        variation_history = []
        completed_elements = Completed_element.objects.filter(completed_workout__user__id = user_id, variation__id = variation.id).order_by('-completed_workout__workout_class__date')
        if len(completed_elements) > 0:
            first = len(completed_elements) - 1
            first = completed_elements[first]
            date = first.completed_workout.workout_class.date.isoformat()
            first_time = {
                "date"      : date,
                "workout"   : first.completed_workout.workout_class.workout.name,
                "reps"      : first.element_used.reps,
                "rounds"    : first.completed_workout.workout_class.workout.rounds,
                }    
        for completed_element in completed_elements:
            if not len(completed_elements) == 0:
                date = completed_element.completed_workout.workout_class.date.isoformat()
                variation_history.append({
                                            "reps" : completed_element.element_used.reps,
                                            "rounds" : completed_element.completed_workout.workout_class.workout.rounds,
                                            "date" : date
                                        })
                count = count + completed_element.element_used.reps
        if not variation_history == []:   
            element_history.append({"variation_name" : variation.name, "variation_history" : variation_history, "count" : count, "first" : first_time})
        total = total + count   
    return_dict = {
            'user_name'         : User.objects.get(id=user_id).first_name,
            'element_name'      : element.name,
            'total'             : total,
            'element_history'    : element_history,
        }
    return return_dict

def user_history(user_id):
    """
    Purpose: Given a user return they're histroy
    Input:
        "user_id"       : The id of the user(INT),
    Output:
        A dictionary of:
        'computed_workouts'         : A list of competed workouts the user has done
                                      "id"      : The completed workout id(INT),
                                      "date"    : The date of the completed workout in YYYY-MM-DD format(STRING),
                                      "workout" : The name the workout done (STRING),
                                      "info"    : type_value
                                                    : type_value if Timed equals {"type" : "Timed", "time": the amount of time it took in secs(INT)}
                                                    : type_value if AMRAP equals {"type" : "AMRAP", "rounds": how many rounds the user did(INT)}
                                                    : type_value if Done equals  {"type" : "Done"}
        'workout_count'             : The number of crossfit workouts the user has loged(INT)
        'total_all_elements_count'  : The number of total reps a user has done (INT)
        'all_elements_count'        : A list of element the user has done(LIST)
                                      "name"  : The name of the element
                                      "count" : How many times the user has done the element 
                                    
    """
    total_all_elements_count = 0
    completed_workouts = Completed_workout.objects.filter(user__id = user_id).order_by('-workout_class__date')
    completed_workout_list = []
    for workouts in completed_workouts:
        type_name = Workout.objects.get(id= workouts.workout_class.workout.id).workout_type.name
        if type_name == "Timed":
            type_value = {"type" : "Timed", "time": workouts.secs}
        elif type_name == "AMRAP":
            type_value = {"type" : "AMRAP", "rounds": workouts.rounds}
        else:
            type_value = {"type" : "Done"}    
        completed_workout_list.append({
            "id"            : workouts.id,
            "date"          : workouts.workout_class.date.isoformat(),
            "workout"       : workouts.workout_class.workout.name,
            "info"          : type_value,
        })           
    workout_count = completed_workouts.count()
    all_elements_count = []
    element_list = Element.objects.all()
    for element in element_list:
        completed_elements_list = Completed_element.objects.filter(element_used__element = element.id)
        element_count = 0
        for completed_element in completed_elements_list:
            element_count = element_count + (completed_element.element_used.reps * completed_element.completed_workout.workout_class.workout.rounds)
        if not element_count == 0:
            all_elements_count.append ({
                        "name"  : element.name,
                        "count" : element_count,
                })
        total_all_elements_count = total_all_elements_count + element_count
    history = {
            "completed_workouts"            : completed_workout_list,
            "workout_count"                 : workout_count,
            "all_elements_count"            : all_elements_count,
            "total_all_elements_count"      : total_all_elements_count,
    }
    return history   














