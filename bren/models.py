import datetime
from django.db import models
from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import simplejson
from crossfit.bren.calcs import*


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
    def __unicode__(self):
        return self.workout.name+ ", "+ self.element.name

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

# -- API METHODS -------------- #
def get_user_info(user_id):
    """
    CURRENTLY UNUSED
    """
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

def get_users(search_str):
    """
    Returns:
    {
       "display_name": <str>,
       "user_name":     <str>,
    }
    # ordered by display_name
    """

    # IF we want to search by last name too... but too confusing I think
    #
    #user_query = User.objects.filter(
    #                    Q(first_name__startswith=search_str) |
    #                    Q(last_name__startswith=search_str)
    #                ).order_by("first_name")[:5]

    user_query = User.objects.filter(
                    first_name__startswith=search_str
                ).order_by("first_name")[:7]


    return [{"display_name": "%s %s" % (user.first_name, user.last_name), "user_name": user.username} for user in user_query]

def check_user_login(username, password):
    """
    Purpose: Verify that a user and password combination will result in a
             successful login if used
    Input:   username : username of a user (STRING)
             password : a raw password (STRING)
    Output:  success (boolean)
    """
    user = User.objects.get(username=username)
    return user.check_password(password)

def get_element(element_id):
    """
    Purpose: Given a element id output element and all its variation
    Input: element_id (INT)
    Output:
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
    for workouts in Completed_workout.objects.filter(workout_class__workout__id__exact= workout_id, user__id__exact=user_id).order_by('-workout_class__date'):
        workout = get_completed_workout_info(workouts.id)
        completed_workouts.append(workout)
    return completed_workouts

def get_completed_workout_info(completed_workout_id):
    """
    Purpose: Given a completed workout id return a dictionary with all the information.
    Input:
        completed_workout_id : the id number for the completed workout to look up.
    Output:
        id              : The id of the completed workout
        user_id         : The id of the user who did the workout,
        user_name       : The first name of the user who did the workout,
    user_last_initial   : The First letter of the Last name of the user who did the workout,
        workout         : The name of the workout
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
        workout.update({"info": type_value})
        
    variations = []    
    for completed_element in Completed_element.objects.filter(completed_workout__id = completed_workout_id).order_by('element_used__order'):
            variations.append({"element": completed_element.variation.element.name , "variation": completed_element.variation.name})
    
    data = {
        "id" : completed_workout_id,
        "user_id" : completed_workout.user.id,
        "user_name": User.objects.get(id=completed_workout.user.id).first_name,
        "user_last_initial" : User.objects.get(id=completed_workout.user.id).last_name[0],
        "workout" : completed_workout.workout_class.workout.name,
        "date" : completed_workout.workout_class.date.isoformat(),
        "info" : type_value,
        "variations" : variations,
        }
    return data

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

def get_workouts(date):
    """
    Purpose: Given a date output what workouts happend
    Input:
            date     : The date in YYYY-MM-DD format (STRING)
    Output:
            A list of   : Workouts that happend that day
            "name"      : The name of the workout(STRING)
            "id"        : The id of the workout
    """
    date = datetime.datetime.strptime(date, DATE_FORMAT)
    workouts = {}
    workout_class_list = []
    for classes in Workout_class.objects.filter(date__exact=date):
        if not classes.workout.name in workouts:
            workout_class_list.append ({"name": classes.workout.name , "id": classes.workout.id})
            workouts.update({classes.workout.name : 1})
        return_dict = {
            "workout_list": workout_class_list,
        }
    return return_dict
def get_week_roster(date):
    """
    Purpose: Given a date return the weeks classes and the people that did them.
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
    Purpose: Given a dictionary of a completed workout to be saved, save it
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

def user_done_class(user_id, workout_id, date):
    """
    Purpose: Given a user and date and a workout
    Input:
        "user_id"               : The id of the user(INT),
        "workout_id"            : The id of the workout(INT),
        "date"                  : The date of the workout as YYYY-MM-DD
    Output: The completed workout or None if they haven't done it
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
    Input:
        "user_id"               : The id of the user(INT),
        "workout_class_id"      : The id of the workout class(INT)

    Output:
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
        if variation.element_used.element.weighted == True:
            variation_id = int(variation.variation.name)
        else:
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
    Input:
        "element_id"    : The id of the element that is weighted(INT)
        "weight"        : The amount of weight in lbs(INT)
    Output:
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
        'total_time'               : The total amount of time of working out loged in Sec (INT)
        'total_all_elements_count'  : The number of total reps a user has done (INT)
        'all_elements_count'        : A list of element the user has done(LIST)
                                      "name"  : The name of the element
                                      "count" : How many times the user has done the element

    """
    total_time = 0
    total_all_elements_count = 0
    completed_workouts = Completed_workout.objects.filter(user__id = user_id).order_by('-workout_class__date')
    completed_workout_list = []
    for workouts in completed_workouts:
        type_name = Workout.objects.get(id= workouts.workout_class.workout.id).workout_type
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
        total_time = total_time + workouts.secs
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
            "total_time"                    : total_time,
            "all_elements_count"            : all_elements_count,
            "total_all_elements_count"      : total_all_elements_count,
    }
    return history

def get_workout_with_date_class(date, class_id):
    """
    Purpose: Given a class id return the workout information of that class
    Input:
        "date"      : The date of the class YYYY-MM-DD
        "class_id"  : The id of the class(INT),

    Output:
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
# -- Reports --------------------- #
def user_week(user_id, date):
    date = datetime.datetime.strptime(date, DATE_FORMAT).date()
    days = []
    datedelta = datetime.timedelta(days=1)
    while not date.weekday() == 6:
        date = date - datedelta
        i = 0
    while i <= 6:
        days.append ({"day": get_weekday(i), "day_workouts": []})
        i = i + 1
    startweek = date
    for day in days:
        workouts = []
        variations = []
        for completed_workout in Completed_workout.objects.filter(user__id = user_id, workout_class__date = date):
            for completed_element in Completed_element.objects.filter(completed_workout__id = completed_workout.id).order_by('element_used__order'):                
                variations.append ({ "element" : completed_element.element_used.element.name, "variation" : completed_element.variation.name})
            type_name = completed_workout.workout_class.workout.workout_type
            if type_name == "Timed":
                type_value = {"type" : "Timed", "time": completed_workout.secs}
            elif type_name == "AMRAP":
                type_value = {"type" : "AMRAP", "rounds": completed_workout.rounds}
            else:
                type_value = {"type" : "Done"}
            workouts.append({
                "name" : completed_workout.workout_class.workout.name,
                "variations" : variations,
                "type_value" : type_value,  
            })
        if workouts == []:
            day['day_workouts'] = 0
        else:    
            day['day_workouts'] = workouts
        date = date + datedelta
    data = {
        "week_end"      : date.isoformat(),
        "week_start"    : startweek.isoformat(),
        "user" : User.objects.get(id=user_id).first_name,
        "days" : days,
        }
    return data

def workout_date(workout_id, date):
    date = datetime.datetime.strptime(date, DATE_FORMAT).date()
    workout_type = Workout.objects.get(id=workout_id).workout_type
    if workout_type == "Timed":
        completed_workouts = Completed_workout.objects.filter(workout_class__workout__id = workout_id, workout_class__date = date).order_by('secs')
    if workout_type == "AMRAP":
        completed_workouts = Completed_workout.objects.filter(workout_class__workout__id = workout_id, workout_class__date = date).order_by('-rounds')    
    workouts = []
    for co in completed_workouts:
        workouts.append(get_completed_workout_info(co.id))
        
    elements = []
    for element in Element_used.objects.filter(workout__id = workout_id).order_by('order'):
        elements.append(element.element.name)
        
    data = {
    "id" : workout_id,
    "type" : Workout.objects.get(id=workout_id).workout_type,
    "workout" : Workout.objects.get(id=workout_id).name,
    "date" : date.isoformat(),
    "workouts" : workouts,
    "elements" : elements,
    }
    return data


#-- Tools ----------------------#
def create_db_variations(element_name):
    weight = 5
    try:
        element = Element.objects.get(name = element_name)
    except:
        return "No Element named " + element_name
    while (weight < 50):
        variation = Variation ()
        variation.name = str(weight) + " lbs"
        variation.element = element
        variation.save ()
        weight = weight + 5