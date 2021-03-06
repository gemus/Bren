from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'crossfit.bren.views.index'),
    # /workout_form/<date>/<class_id>        /workout_form/2009-11-21/3
    (r'^workout_form/(\d{4}-\d{2}-\d{2})/(\d+)/$', 'crossfit.bren.views.workout_form'),
    (r'^workout_form/(\d{4}-\d{2}-\d{2})/None/$', 'crossfit.bren.views.no_workout_found'),

    (r'^save_workout/$', 'crossfit.bren.views.save_workout'),

    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),

    (r'^json_api/$', 'crossfit.bren.api.json_api'),
)