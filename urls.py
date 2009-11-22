from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^index/$', 'Crossfit.Bren.views.index'),
    # /workout_form/<date>/<class_id>        /workout_form/2009-11-21/3
    (r'^workout_form/(\d{4}-\d{2}-\d{2})/(\d+)/$', 'Crossfit.Bren.views.workout_form'),
    (r'^workout_form/(\d{4}-\d{2}-\d{2})/None/$', 'Crossfit.Bren.views.no_workout_found'),
    (r'^json_api/$', 'Crossfit.Bren.views.json_api'),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )