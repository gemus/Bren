import datetime
from django.core.management.base import NoArgsCommand, CommandError

from crossfit.email_sender.models import UserEmailPermissions, get_subscribed_users
from crossfit.email_sender.sender import email_user
from crossfit.reports import reports

# TODO : Add cron command that goes along with this

class Command(NoArgsCommand):
    help = "Emails out a weekly report to all users who have subscribed"

    def handle_noargs(self, **options):
        start_date = datetime.datetime(2010, 1, 1)
        end_date = datetime.datetime(2010, 2, 20)
        for user in get_subscribed_users():
            print "USER", user
            data = reports.completed_workouts(start_date, end_date, user)
            email_user(user, 'Workout Report', 'reports/completed_workouts.html', data)

        print "GET TO DA EMAIL!"
        #raise CommandError("I'm an error that something went wrong")