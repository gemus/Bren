import datetime
from django.core.management.base import NoArgsCommand, CommandError

from crossfit.email_sender.models import UserEmailPermissions, get_subscribed_users
from crossfit.email_sender.sender import email_user
from crossfit.reports import reports

# TODO : Add cron command that goes along with this

class Command(NoArgsCommand):
    help = "Emails out a weekly report to all users who have subscribed"

    def handle_noargs(self, **options):
        # Date range of the last 7 days
        start_date = datetime.datetime.combine(datetime.date.today(), datetime.time())
        end_date = start_date - datetime.timedelta(days=7)

        for user in get_subscribed_users():
            print "USER", user
            data = reports.completed_workouts(start_date, end_date, user)
            email_user(user, 'Workout Report', 'reports/completed_workouts.html', data)

        print "GET TO DA EMAIL!"
        #raise CommandError("I'm an error that something went wrong")