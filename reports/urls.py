from django.conf.urls.defaults import *

# URLs take the form /<user_id>/<report_name>/<param>-<param>-.../

urlpatterns = patterns('',
    (r'^$', 'crossfit.reports.views.index'),

    # <user_id>/weekly_report/<year>-<week_num>/
    (r'^(\d+)/weekly_report/(\d+)-(\d+)/$', 'crossfit.reports.views.weekly_report'),
)
