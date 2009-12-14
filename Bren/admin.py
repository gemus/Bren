from Crossfit.Bren.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
 
class Completed_elementInline(admin.StackedInline):
    model = Completed_element
    
class Workout_elementInline(admin.StackedInline):
    model = Element_used 

class Element_usedAdmin(admin.ModelAdmin):    
    list_display = ('workout', 'element','reps', 'order')
    fields = ['workout', 'element', 'reps' , 'order']
    list_filter = ['workout', 'element']

class Workout_classAdmin(admin.ModelAdmin):    
    list_display = ('date', 'workout', 'class_info')
    fields = ['date', 'workout', 'class_info']
    list_filter = ['date', 'workout', 'class_info']

class Completed_workoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_class', 'secs', 'rounds')
    fields = ['user', 'workout_class', 'secs', 'rounds']
    list_filter = ['user', 'workout_class', 'rounds']
    inlines = [Completed_elementInline]

    def day_of_week(self, completed_workout):
        return get_weekday(completed_workout.date.weekday())
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('element', 'name')
    list_filter = ['element']

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'comments', 'workout_type', 'time', 'rounds')
    fields = ['name', 'comments', 'workout_type', 'time', 'rounds']
    inlines = [Workout_elementInline]

class Completed_elementAdmin(admin.ModelAdmin):
     list_display = ('completed_workout', 'variation')
     list_filter = ['variation']

     def user_name(self, variation):
         return variation.completed_workout.user

     def workout_name(self, workout):
         return workout.completed_workout.workout
        
     def workout_date(self, variation):
         return variation.completed_workout.date

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(UserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Class_info)
admin.site.register(Workout_class, Workout_classAdmin)
admin.site.register(Completed_workout, Completed_workoutAdmin)
admin.site.register(Element)
admin.site.register(Element_used, Element_usedAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Completed_element, Completed_elementAdmin)





