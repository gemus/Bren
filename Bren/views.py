from django.template import Context, loader
from Crossfit.Bren.models import *
from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import *
import datetime
from django import forms
from django.contrib.auth import authenticate, login, logout

def fun(request):
    t = loader.get_template('Bren/veiw.html')
    user_list = User.objects.all()
    user = User.objects.get(id=1)
    completed_workout_list = Completed_workout.objects.filter(user__exact=user)
    c = Context({
            'completed_workout_list' : completed_workout_list,
            'user_list': user_list,
            'user': user,
        })
    return HttpResponse(t.render(c))


def index(request):
    t = loader.get_template('index/index.html')
    c = Context((
    ))
    return HttpResponse(t.render(c))

def user_index(request):   
    if (request.user.is_staff):
        user_list = User.objects.all()
        t = loader.get_template('index/user_index.html')
        c = Context({
            'user_list': user_list,
        })
        return HttpResponse(t.render(c))
    else:
        return HttpResponse("You don't have Permission to Veiw this")

def user_info(request,user_id):
    user = request.user
    if (user == User.objects.get(id=user_id)):
        completed_workout_list = Completed_workout.objects.filter(user__id__exact=user.id)
        t = loader.get_template('user/Completed_workout_list.html')
        c = Context({
            'completed_workout_list': completed_workout_list,
            'user': user,
        })
        return HttpResponse(t.render(c))
    else:
        return HttpResponse("You don't have Permission to Veiw this")

def input_workout(request, user_id):
    user = request.user
    if (user == User.objects.get(id=user_id)):
        workout_class = Workout_class.objects.get(id=3)# this will be the user sleected workout
        workout = workout_class.workout
        element_used_list = Element_used.objects.filter(workout__id__exact = workout.id).distinct()
        variation_list = []
        for workout_element in element_used_list:
            variation_list += Variation.objects.filter(element__exact = workout_element.element)

        variation_list = list(set(variation_list))
        
        t = loader.get_template('user/input.html')
        c = Context({
            'workout_class' : workout_class,
            'element_used_list' : element_used_list,
            'user': user,
            'variation_list' : variation_list,
        })
        return HttpResponse(t.render(c))
    return HttpResponse("You don't have Permission to Veiw this")

def completed_workout_page(request, user_id, completed_workout_id):
    completed_workout = Completed_workout.objects.get(id = completed_workout_id)
    user = request.user
    variation_used_list = Variation_used.objects.filter(completed_workout__id__exact = completed_workout.id)
    element_used_list = Element_used.objects.filter(workout__id__exact = completed_workout.workout_class.workout.id)
    t = loader.get_template('user/Completed_workout_info.html')
    c = Context({
        'completed_workout': completed_workout,
        'user' : user,
        'variation_used_list' : variation_used_list,
        'completed_workout' : completed_workout,
        'element_used_list' : element_used_list,
    })
    return HttpResponse(t.render(c))
    
def roster(request):
    if (request.user.is_staff):
        dates_list = Workout_class.objects.values('date').distinct()
        t = loader.get_template('trainer/dates.html')
        c = Context({
            'dates_list': dates_list,
        
        })
        return HttpResponse(t.render(c))
    else:
        return HttpResponse("You don't have Permission to Veiw this")

def get_classes(request, date):
    if (request.user.is_staff):
        workout_class_list = Workout_class.objects.filter(date__exact=date).distinct()    
        t = loader.get_template('trainer/workout_times.html')
        c = Context({
            'workout_class_list': workout_class_list,
        })
        return HttpResponse(t.render(c))
    else:
        return HttpResponse("You don't have Permission to Veiw this")

def class_roster(request, workout_class_id):
    if (request.user.is_staff):
        completed_workout_list = Completed_workout.objects.filter(workout_class__id = workout_class_id)
        if completed_workout_list:
            workout = completed_workout_list[0].workout_class.workout
        else:
            workout = []
        t = loader.get_template('trainer/class_roster.html')
        c = Context({
            'completed_workout_list': completed_workout_list,
            'workout': workout
        
        })
        return HttpResponse(t.render(c))
    else:
        return HttpResponse("You don't have Permission to Veiw this")

class Completed_workoutForm(forms.Form):
    mins = forms.IntegerField()
    secs = forms.IntegerField()
    rounds = forms.IntegerField()

def save_info(request):
    if request.method == 'POST': # If the form has been submitted...
        form = Completed_workoutForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            co = Completed_workout()               
            co.user = request.user
            co.mins = request.POST['mins']
            co.secs = request.POST['secs']
            co.rounds = request.POST['rounds']
            co.workout_class = Workout_class.objects.get(id=request.POST['workout_class_id'])
            co.save()
            variation_counter = 0
            variation_ids = []

            while "variation_%d" % variation_counter in request.POST:
                variation_ids.append(request.POST["variation_%d" % variation_counter])
                variation_counter += 1
            variations = [Variation.objects.get(id=x) for x in variation_ids]
            for variation in variations:
                v_u= Variation_used()
                v_u.variation = variation
                v_u.completed_workout = co
                v_u.completed_workout
                v_u.save()
            
            return HttpResponse("Awesome")
        else:
            return HttpResponse("BAD")

def user_login(request):
    t = loader.get_template('index/login.html')
    c = Context((
    ))
    return HttpResponse(t.render(c))

def user_info(request, user_id):
    if (request.user.is_staff):
        user = User.objects.get(id=user_id)
        t = loader.get_template('user/User_info.html')
        c = Context({
            'user': user,     
        })
        return HttpResponse(t.render(c))
    else:
        return HttpResponse("you don't have permission to do this")


class Log_inForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField()

def login_check(request):
    if request.method == 'POST':
        form = Log_inForm(request.POST)
        if form.is_valid():          
            user = authenticate(username=request.POST['user_name'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("LOGED IN")
                else:
                    return HttpResponse("Your Account is not active")
            else:
                return HttpResponse("You have entered a invalid User name or password")
        else:
            t = loader.get_template('index/login.html')
            c = Context((
            ))
            return HttpResponse(t.render(c))
    return HttpResponse("Nothing posted")
    
