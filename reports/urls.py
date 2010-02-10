from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'crossfit.reports.views.index'),
)
