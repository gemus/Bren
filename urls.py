from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import django.contrib.auth.views

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'crossfit.bren.views.index'),
    # /workout_form/<date>/<class_id>        /workout_form/2009-11-21/3
    (r'^workout_form/(\d{4}-\d{2}-\d{2})/(\d+)/$', 'crossfit.bren.views.workout_form'),
    (r'^workout_form/(\d{4}-\d{2}-\d{2})/None/$', 'crossfit.bren.views.no_workout_found'),

    (r'^save_workout/$', 'crossfit.bren.views.save_workout'),

    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),

    (r'^json_api/$', 'crossfit.bren.views.json_api'),
    (r'^admin/', include(admin.site.urls)),

    # trainer stuff
    (r'^weekly_roster/(\d{4}-\d{2}-\d{2})/$', 'crossfit.bren.views.weekly_roster'),

    # Reports
    (r'^report/', 'crossfit.bren.views.display_workout_rank'),
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
