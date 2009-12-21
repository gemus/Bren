from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import django.contrib.auth.views

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'crossfit.Bren.views.index'),
    # /workout_form/<date>/<class_id>        /workout_form/2009-11-21/3
    (r'^workout_form/(\d{4}-\d{2}-\d{2})/(\d+)/$', 'crossfit.Bren.views.workout_form'),
    (r'^workout_form/(\d{4}-\d{2}-\d{2})/None/$', 'crossfit.Bren.views.no_workout_found'),

    (r'^save_workout/$', 'crossfit.Bren.views.save_workout'),

    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),

    (r'^json_api/$', 'crossfit.Bren.views.json_api'),
    (r'^admin/', include(admin.site.urls)),

    # trainer stuff
    (r'^weekly_roster/(\d{4}-\d{2}-\d{2})/$', 'crossfit.Bren.views.weekly_roster'),
    (r'^create_user/', 'crossfit.Bren.views.create_user'),
    (r'^save_user/', 'crossfit.Bren.views.save_user'),

    # Development stuff
    (r'^full_element_history/(?P<user_id>\d+)/(?P<element_id>\d+)/$', 'crossfit.Bren.views.full_element_history'),
    (r'^user_history/', 'crossfit.Bren.views.user_history'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
