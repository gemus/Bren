from django.core.management.base import NoArgsCommand, CommandError

from crossfit.email_sender.models import UserEmailPermissions, get_subscribed_users

# TODO : Add cron command that goes along with this

class Command(NoArgsCommand):
    help = "Emails out a weekly report to all users who have subscribed"

    def handle_noargs(self, **options):
        for i in get_subscribed_users():
            print i

        print "GET TO DA EMAIL!"
        #raise CommandError("I'm an error that something went wrong")