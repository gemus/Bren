from django.conf.urls.defaults import *

# URLs take the form /<user_id>/<report_name>/
# Get parameters not not handled by urls

urlpatterns = patterns('crossfit.reports.views',
    (r'^$', 'index'),

    # /<user_name>/completed_workouts/?start_date=2010-01-01&end_date=2010-01-07
    (r'^(\w+)/completed_workouts/$', 'completed_workouts'),
    (r'^attendence/(\d{4}-\d{2}-\d{2})/$', 'attendence'),
    (r'^ranking/(\d+)/$', 'ranking'),

)