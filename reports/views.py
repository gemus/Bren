from django.shortcuts import render_to_response
from django.contrib.auth.models import User

"""
=== Design Philosophy =========================================================
Each view is a report, and heavily tied to the queries. So no point in
separating out the model calls into its own module. Each view will define its
own set of queries to be sent directly to the template.

If there is a lot of code reuse that we can do from the reports (which I
currently doubt), then it will make sense to separate them into their own
module.
"""

# Instead of getting a user_id get a User object as the 2nd param
def report_user(func):
    def new_func(*args, **kw):
        user = User.objects.get(pk=int(args[1]))
        return func(args[0], user, *args[2:], **kw)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func

def index(request):
    return render_to_response('reports/index.html')

@report_user
def weekly_report(request, user, year, week_num):
    print user
    return render_to_response('reports/weekly_report.html')