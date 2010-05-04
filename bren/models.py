import re
import datetime
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import simplejson
from django.db.models import Count
from django.db.models import Q


DATE_FORMAT = "%Y-%m-%d"
workout_choices = (
    ('Timed', 'Timed'),
    ('AMRAP', 'AMRAP'),
    ('Done', 'Done'),
    )

class Workout(models.Model):
    """
    Purpose:            The actual workout information
    Fields:
            name        : The name of the workout (STRING)
            comments    : Any comments the trainer wants to add about the workout(STRING)
            workout_type: What style of workout is it(Choice field)
            time        : The amount of time allowed for a AMRAP workout(INT number of mins)
            rounds      : How many rounds of the workout is required(INT)
    """
    name = models.CharField(max_length=20)
    comments = models.CharField(max_length=200, blank = True)
    workout_type = models.CharField(max_length=200, choices = workout_choices)
    time = models.IntegerField()
    rounds = models.IntegerField()
    def __unicode__(self):
        return self.name

class Class_info(models.Model):
    """
    Purpose : A actualy class in the day. i.e.  "6:00 Crosfit"
    Fields:
            title        : The name of the class(STRING)
    """
    title = models.CharField(max_length=30)
    def __unicode__(self):
        return self.title

class Workout_class(models.Model):
    """
    Purpose : Sets workout to a date and class
    Fields:
            date        : The date of the workout is happening(DATE)
            workout     : A pointer to the workout is happpening(POINTER)
            class_info  : A pointer to which class is doing it(POINTER)
    """
    date = models.DateField('Date Completed')
    workout = models.ForeignKey(Workout)
    class_info = models.ForeignKey(Class_info)
    def __unicode__(self):
        return self.workout.name+ " "+self.class_info.title + " " +self.date.isoformat()

class Completed_workout(models.Model):
    """
    Purpose : The basic information about a completed workout
    Fields:
            secs            : How many secs it took(INT)
            user            : A pointer to which user did the workout(POINTER)
            workout_class   : A pointer the workout class that was done(POINTER)
            rounds          : How many rounds waas done(INT)
    """
    secs = models.IntegerField()
    user = models.ForeignKey(User)
    workout_class = models.ForeignKey(Workout_class)
    rounds = models.IntegerField()

class Element(models.Model):
    """
    Purpose : The element info
    Fields:
            name            : The name of the element(STRING)
    """
    name = models.CharField(max_length=20)
    weighted = models.BooleanField()
    def __unicode__(self):
        return self.name

class Element_used(models.Model):
    """
    Purpose : A element of a workout
    Fields:
            workout         : A pointer to which workout is using it(POINTER)
            element         : A pointer to which element is being used(POINTER)
            reps            : The number of reps that is requird (INT)
            order           : Which posision it is in the workout (INT)
    """
    workout = models.ForeignKey(Workout)
    element = models.ForeignKey(Element)
    reps = models.IntegerField()
    order = models.IntegerField()
class Variation(models.Model):
    """
    Purpose : A Variation to a workout
    Fields:
            name            : What the variation is called
            element         : A pointer to which element for the variation (POINTER)

    """
    name = models.CharField(max_length=20)
    element = models.ForeignKey(Element)
    def __unicode__(self):
        return self.element.name+ ", "+ self.name

class Completed_element(models.Model):
    """
    Purpose : The information about somone doing a element
    Fields:
            completed_workout   : What the variation is called
            element_used             : A pointer to which element for the variation (POINTER)
            variation           : A pointer to which variation is being used (POINTER)
    """
    completed_workout = models.ForeignKey(Completed_workout)
    element_used = models.ForeignKey(Element_used)
    variation= models.ForeignKey(Variation)
    def __unicode__(self):
        return self.completed_workout.user.username+ ", "+self.completed_workout.workout_class.workout.name+  ", "+ self.variation.name + ", " + self.element_used.element.name

class UserProfile(models.Model):
    """
    Purpose : Additional information about the user that should be saved
    Fields:
    """
    user = models.ForeignKey(User, unique=True)

# =============================================
# = Model Methods =============================
# =============================================
def get_users(search_str, num_results, search_type = "contains"):
    """
    Purpose: Searches users based on first name using "strats_with" logic
    Params: search_str <string>
            num_results <int> (-1 returns all)
    Returns: Array of dictionaries with display_name, user_name keys
        [{ "display_name": <str>, "user_name": <str>},...]
    # ordered by display_name
    """

    if search_type == "starts_with":
        user_query = User.objects.filter(
                        first_name__istartswith=search_str
                    ).order_by("first_name")

    if search_type == "contains":
        user_query = User.objects.filter(
            Q(first_name__istartswith=search_str) | 
            Q(last_name__istartswith=search_str)
            ).order_by("first_name")
    
   
    # Are we limiting results?
    if num_results > 0:
        user_query = user_query[:num_results]

    return [{"display_name" : "%s %s" % (user.first_name, user.last_name),
             "user_name"    : user.username}
                    for user in user_query]

def get_user(user_name):
    """
    Purpose: Return user information given an id
    Params: user_name <string>
    Returns: Dictionary containing user information
    """

    user = User.objects.get(username__exact=user_name)

    return { 'first_name'  : user.first_name,
             'last_name'   : user.last_name,
             'email'       : user.email,
             'last_login'  : user.last_login.strftime(DATE_FORMAT),
             'date_joined' : user.date_joined.strftime(DATE_FORMAT) }

def update_user(user_dict):
    user = User.objects.get(username__exact=user_dict['user_name'])

    # Validate the keys
    # TODO : This should be done in the views
    del(user_dict['user_name'])
    allowed_keys = set(['first_name', 'last_name', 'email', 'password'])
    if len(set(user_dict.keys()) - allowed_keys) != 0:
        return "fail - Unexpected keyword %s" % (set(user_dict.keys()) - allowed_keys).pop()

    # Change the password if requested, then remove key.
    # Bad things happen if you set the password attribute on a user directly
    if 'password' in user_dict:
        user.set_password(user_dict['password'])
        del user_dict['password']

    # Do the updating
    for key, value in user_dict.items():
        setattr(user, key, value)
    user.save()
    return "success"

def create_user(user_dict):
    user_name = "DPL_%s_%s" % (user_dict['first_name'], user_dict['last_name'])
    user_name = re.sub("\W", "", user_name)

    user_dict['user_name'] = user_name

    user = User(username=user_name)
    user.save()

    update_user(user_dict)
    return user_name

def delete_user(user_name):
    User.objects.get(username__exact=user_name).delete()
    return "success"

def check_user_login(username, password):
    """
    Purpose: Verify that a user and password combination will result in a
             successful login if used
    Params:   username : username of a user (STRING)
             password : a raw password (STRING)
    Returns:  success (boolean)
    """
    user = User.objects.get(username=username)
    return user.check_password(password)

def get_element(element_id):
    """
    Purpose: Given a element id output element and all its variation
    Params: element_id (INT)
    Returns:
            "id"        : The id of the element (INT)
            "name"      : The name of the element (STRING)
            "type"      : one of "variation" | "weight" | "regular" (STRING)
            "variations : A list of variation dictionarys contaiting(LIST)
                          "id" : The of the variation(INT)
                          "name" : The name of the variation(STRING)
    """
    elm = Element.objects.get(id=element_id)
    variations = []
    for variation in Variation.objects.filter(element__id = elm.id):
        variations.append({"id": variation.id, "name": variation.name})

    if elm.weighted:
        elem_type = "weight"
    elif len(variations) > 0:
        elem_type = "variation"
    else:
        elem_type = "regular"

    element = {"id": elm.id, "name": elm.name, "type": elem_type, "variations": variations}
    return element

def get_workout(workout_date_str, class_id):
    """
    Purpose: Given a workout date and class return the workout data
    Params:
        workout_date_str : The date of the workout in YYYY-MM-DD format (STRING)
        class_id : the class id (INT)

    Returns:
        "id"           : The workout id (INT)
        "name"         : The workout name (STRING)
        "comments"     : The workout comment (STRING)
        "time"         : The time allowed for a AMRAP workout(INT)
        "rounds"       : The number of rounds for the workout(INT)
        "workout_type" : The type of workout AMRAP, TIMES, DONE ect.
        "elements"     : A list of all the elements in a workout
                         "reps"         : Number of reps for the element (INT)
                         "order"        : Order to be done (INT)
                         "element"      : An element structure that follows:
                             "id"           : element id,
                             "name"         : element name,
                             "type"         : one of "variation" | "weight" | "regular"
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
        for elm_used in workout.element_used_set.all().order_by('order'):
            elements.append({"reps": elm_used.reps,
                             "order": elm_used.order,
                             "element": get_element(elm_used.element.id)})
        return_dict = {
                        "id"           : workout.id,
                        "name"         : workout.name,
                        "comments"     : workout.comments,
                        "time"         : workout.time,
                        "rounds"       : workout.rounds,
                        "workout_type" : workout.workout_type,
                        "elements"     : elements,
                        "class_name"   : Class_info.objects.get(pk=int(class_id)).title,
                        "workout_class": workouts[0].id,
                      }
        return return_dict
    return {"error": "No Class Found"}

def get_workouts(date):
    """
    Purpose: Given a date return the workouts that happened that day
    Params:
            "date"      : The date of the workout in YYYY-MM-DD format (STRING)
    Returns:
            "workouts"  : A list of the workouts that happened that day(LIST)
                        "workout_name" : the workout name,
                        "orkout_id"    : The id of the workout,
    """
    date = datetime.datetime.strptime(date, DATE_FORMAT)
    workout_index = {}
    workouts = []
    for workout_class in Workout_class.objects.filter(date = date):
        if not workout_class.workout.id in workout_index:
            workout_index.update({workout_class.workout.id : 2})
            workouts.append({
            "workout_name" : workout_class.workout.name,
            "workout_id" : workout_class.workout.id,
            })
        
    return workouts
    

def get_element_history(user_id, element_id):
    """
    Purpose: Given a user and element return the users history with the element in list form
    Params:
            user_id : user's id as (INT)
    Returns:
            A List of       : Times the user has done the element

            "workout"       : The name of the workout the each element is coming from(STRING)
            "rounds"        : How many round of reps for the element(INT)
            "reps"          : How many reps per round of the element(INT)
            "variation"     : The name of the variation on the element(STRING)
            "variationn_id" : The id of the variation (INT)
    Or Returns:
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
    Params:
            user_id     : The users id (INT)
            workout_id  : The workouts id (INT)
    Returns:
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

def get_completed_workout(user_id, workout_id):
    """
    Purpose: Given a user and a workout return times the user has done the workout
    Params:
            user_id     : The users id (INT)
            workout_id  : The workout id (INT)
    Returns:
            A List of   : Times the user has done the workout

            "id"        : The id of the completed workout(INT)
            "name"      : The name of the workout(STRING)
            "date"      : The date they did the workout in YYYY-MM-DD format(STRING)
            "info"      : The information about type of workout and score based on that {"info": type_value} (DICT)
                        : type_value if Timed equals {"type" : "Timed", "time": the amount of time it took in secs(INT)}
                        : type_value if AMRAP equals {"type" : "AMRAP", "rounds": how many rounds the user did(INT)}
                        : type_value if Done equals  {"type" : "Done"}
         "variations"   : a list of the variations that the user inputed as ("element" : The name of the element(STRING), "variation" : the name of the variation used(STRING)}

    """
    completed_workouts = []
    for workouts in Completed_workout.objects.filter(workout_class__workout__id__exact= workout_id, user__id__exact=user_id).order_by('-workout_class__date'):
        workout = get_completed_workout_info(workouts.id)
        completed_workouts.append(workout)
    return completed_workouts

def get_completed_workout_info(completed_workout_id):
    """
    Purpose: Given a completed workout id return a dictionary with all the information.
    Params:
        completed_workout_id : the id number for the completed workout to look up.
    Returns:
        name            : The name of the workout
        date            : The date of the workout
        info            : The information about type of workout and score based on that {"info": type_value} (DICT)
                        : type_value if Timed equals {"type" : "Timed", "time": the amount of time it took in secs(INT)}
                        : type_value if AMRAP equals {"type" : "AMRAP", "rounds": how many rounds the user did(INT)}
                        : type_value if Done equals  {"type" : "Done"}
        variations      : a list of the variations that the user inputed as ("element" : The name of the element(STRING), "variation" : the name of the variation used(STRING)}
    """
    completed_workout = Completed_workout.objects.get(id=completed_workout_id)

    type_name = completed_workout.workout_class.workout.workout_type
    if type_name == "Timed":
        type_value = {"type" : "Timed", "time": completed_workout.secs}
    elif type_name == "AMRAP":
        type_value = {"type" : "AMRAP", "rounds": completed_workout.rounds}
    else:
        type_value = {"type" : "Done"}

    variations = []
    for completed_element in Completed_element.objects.filter(completed_workout__id = completed_workout_id).order_by('element_used__order'):
            if completed_element.variation.element.weighted == True:
                variation = str (completed_element.variation.name) + " lbs."
            else :
                variation = completed_element.variation.name
            variations.append({"element": completed_element.variation.element.name,
                               "variation": variation,
                               "rounds":    completed_element.element_used.reps})

    data = {
        "name" : completed_workout.workout_class.workout.name,
        "user_name" : completed_workout.user.first_name,
        "comments" : completed_workout.workout_class.workout.comments,
        "date" : completed_workout.workout_class.date.isoformat(),
        "info" : type_value,
        "variations" : variations,
        }
    return data

def get_classes(date):
    """
    Purpose: Given a date output what classes happend
    Params:
            date     : The date in YYYY-MM-DD format (STRING)
    Returns:
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

def create_completed_workout(create_dict):
    """
    Purpose: Given a dictionary of a completed workout to be saved, save it
    Params:
        "user_id"   : The id of the user that did the workout(INT),
        "time"      : The amount of time the workout took if its Timed in seconds(INT)
        "rounds"    : The rounds of the workout the user did if its AMRAP(INT),
        "date"      : The date of the workout in YYYY-MM-DD format (STRING)
        "class_id"  : The workout class id (INT)
        "variations": A list of the variations of the workout as
                      "order"       : what spot in order of the workout the element is in (INT),
                      "variation_id": The id of the variation(INT),
                      "element_id"  : the id of the element(INT)}

    Returns:
    """
    date = datetime.datetime.strptime(create_dict['date'], DATE_FORMAT).date()
    workout_class_id = Workout_class.objects.filter(date=date).get(class_info__id = create_dict['class_id']).id
    workout = Workout_class.objects.get(id=workout_class_id).workout
    if len(Completed_workout.objects.filter(user__id =create_dict['user_id'], workout_class__date = create_dict['date'], workout_class__workout__id = workout.id)) == 0:
        co = Completed_workout()
    else :
        co = Completed_workout.objects.filter(user__id =create_dict['user_id'], workout_class__date = create_dict['date'], workout_class__workout__id = workout.id)
        co = co[0]
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

        element = Element_used.objects.filter(workout__id = workout.id).get(order = variation['order']).element
        if element.weighted == True:
            ce.variation = Variation.objects.get(id = weight_element(element.id, variation['variation_id']))
        else:
            ce.variation = Variation.objects.get(id = variation['variation_id'])
        ce.element_used = Element_used.objects.filter(workout__id = workout.id).get(order = variation['order'])
        ce.save()

def user_done_class(user_id, workout_id, date):
    """
    Purpose: Given a user and date and a workout
    Params:
        "user_id"               : The id of the user(INT),
        "workout_id"            : The id of the workout(INT),
        "date"                  : The date of the workout as YYYY-MM-DD
    Returns: The completed workout or None if they haven't done it
    """
    date = datetime.datetime.strptime(date, DATE_FORMAT).date()
    done = Completed_workout.objects.filter(user__id = user_id, workout_class__date = date, workout_class__workout__id = workout_id)
    if not len(done) == 0:
        return done[0]
    else:
        return None

def get_workout_variations(user_id, workout_class_id):
    """
    Purpose: Given a user id and workout class id create a dictionary that will set the variations
    Params:
        "user_id"               : The id of the user(INT),
        "workout_class_id"      : The id of the workout class(INT)

    Returns:
        A dictionary of
        elements of the workouts form style      The variation that they previously selected of saved
        "varient_ element.id_elements.order"    : variation.id(INT)
    """
    workout_class = Workout_class.objects.get(id = workout_class_id)
    date = workout_class.date
    workout = workout_class.workout

    days_workout = Completed_workout.objects.filter(user__id = user_id, workout_class__date = date, workout_class__workout__id = workout.id)
    if not len(days_workout) == 0:
        return get_previous_variations(days_workout[0].id)
    else:
        workout_id = workout.id
        previous_workouts = Completed_workout.objects.filter(workout_class__workout__id = workout_id, user__id = user_id).order_by('-workout_class__date')
        if not len(previous_workouts) == 0:
            return get_previous_variations(previous_workouts[0].id)
        else:
            return get_workout_estimation(user_id, workout_id)


def get_previous_variations(completed_workout_id):
    """
    Purpose: Given a completed workout output the variations used
    Params:
        "completed_workout_id"  : The id of the completed workout(INT),
    Returns:
        A dictionary of
        elements of the workouts form style      The variation that they been saved
        "varient_ element.id_elements.order"    : variation.id
    """
    return_dict = {}
    completed_elements = Completed_element.objects.filter(completed_workout__id=completed_workout_id)
    for variation in completed_elements:
        element = "varient_" + str(variation.element_used.element.id)+ "_"+ str(variation.element_used.order)
        if variation.element_used.element.weighted == True:
            variation_id = int(variation.variation.name)
        else:
            variation_id = variation.variation.id
        return_dict.update ({ element : variation_id })
    return return_dict

def get_workout_estimation(user_id, workout_id):
    """
    Purpose: Given a user and workout select the variation for the form to the last variations they used on each element
    Params:
        "user_id"       : The id of the user(INT),
        "workout_id"    : The id of the workout(INT)
    Returns:
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

            if elements.element.weighted == True:
                variation_id = int(Variation.objects.get(id = element_history[0]['variationn_id']).name)
            else:
                variation_id = element_history[0]['variationn_id']
        else:
            element = "varient_" + str(elements.element.id)+ "_" + str(elements.order)

            if elements.element.weighted == True:
                variation_id = 0
            else:
                variation_id = Variation.objects.filter(element__id = elements.element.id)[0].id

        return_dict.update ({ element : variation_id })
    return return_dict

def weight_element(element_id, weight):
    """
    Purpose: Given a weight and an element find the right variations or create it than return it
    Params:
        "element_id"    : The id of the element that is weighted(INT)
        "weight"        : The amount of weight in lbs(INT)
    Returns:
        "variation_id"  : The id of the element that was created or selected
    """
    elemenet = Element.objects.get(id=1)
    variations = Variation.objects.filter(element__id = element_id)
    for variation in variations:
        try:
            round_weight = int(round(weight, -1))
            if round_weight > weight:
                if round_weight - weight > 3:
                    weight = round_weight - 5
                else:
                    weight = round_weight
            else:
                if  weight - round_weight > 2:
                    weight = round_weight + 5
                else:
                    weight = round_weight
            if weight == int(variation.name[:3]):
                return variation.id
        except:
            continue
    v = Variation()
    v.name = str(weight)
    v.element = Element.objects.get(id=element_id)
    v.save()
    return v.id

def get_workout_with_date_class(date, class_id):
    """
    Purpose: Given a class id return the workout information of that class
    Params:
        "date"      : The date of the class YYYY-MM-DD
        "class_id"  : The id of the class(INT),

    Returns:
            "name"              : The name of the workout(STRING)
            "comments"          : The comments about the workout(STRING)
            "workout_type"      : "Timed" "AMRAP" ect.
            "time"              : The workout time in secs(INT)
            "rounds"            : The amount of rounds(INT)
    """
    date = datetime.datetime.strptime(date, DATE_FORMAT).date()

    workout = Workout_class.objects.get(date = date, class_info__id = class_id).workout
    name = workout.name
    comments = workout.comments
    workout_type = workout.workout_type
    time = workout.time * 60
    rounds = workout.rounds
    return_dict = {
        "name"              : name,
        "comments"          : comments,
        "workout_type"      : workout_type,
        "time"              : time,
        "rounds"            : rounds,
        }
    return return_dict   