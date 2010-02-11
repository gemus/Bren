from django.conf.urls.defaults import *

# URLs take the form /<user_id>/<report_name>/
# Get parameters not not handled by urls

urlpatterns = patterns('crossfit.reports.views',
    (r'^$', 'index'),

    # /1/weekly_report/?start_date=2010-01-01&end_date=2010-01-07
    (r'^(\d+)/completed_workouts/$', 'completed_workouts'),
)
