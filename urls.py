from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^fun/$', 'Crossfit.Bren.views.fun'),
    (r'^index/$', 'Crossfit.Bren.views.index'),
#    (r'^users/$', 'user_index'),
#    (r'^users/(?P<user_id>\d+)/$', 'user_info'),
#    (r'^users/(?P<user_id>\d+)/input/$', 'input_workout'),
#    (r'^users/(?P<user_id>\d+)/(?P<completed_workout_id>\d+)/$', 'completed_workout_page'),
#    (r'^roster/$', 'roster'),
#    (r'^roster/(?P<date>\d{4}-\d{2}-\d{2})/$', 'get_classes'),
#    (r'^roster/(?P<workout_class_id>\d+)/$', 'class_roster'),
#    (r'^users/save_info/$', 'save_info'),
#    (r'^login/$', 'user_login'),

#    (r'^login_check/$', 'login_check'),
#    (r'^userinfo/(?P<user_id>\d+)/$', 'user_info'),
)
