from django.core.management.base import NoArgsCommand, CommandError

# TODO : Add cron command that goes along with this

class Command(NoArgsCommand):
    help = "Emails out a weekly report to all users who have subscribed"

    # Just to make sure this is all working
    def handle_noargs(self, **options):
        print "GET TO DA EMAIL!"
        #raise CommandError("I'm an error that something went wrong")