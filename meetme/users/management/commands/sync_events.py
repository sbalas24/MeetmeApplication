__author__ = 'hacker'
from django.core.management.base import BaseCommand, CommandError
from meetme.users.models import User,MMconnectaccount
from meetme.users.tasks import get_calender_for_user,get_facebook_events,sync_tasks
from social_auth.models import UserSocialAuth
from django_facebook.models import FacebookProfile
class Command(BaseCommand):
    help = 'Creates a bunch of test users for testing'

    def handle(self, *args, **options):
        for i in UserSocialAuth.objects.all():
            get_calender_for_user.delay(i.user_id)
        for i in UserSocialAuth.objects.all():
            for j in MMconnectaccount.objects.filter(contact = i.user):
                if j.approved:
                    sync_tasks.delay(j.user,i.user)
        for i in FacebookProfile.objects.all():
            get_facebook_events.delay(i.user_id)
        for i in FacebookProfile.objects.all():
            for j in MMconnectaccount.objects.filter(contact = i.user):
                if j.approved:
                    sync_tasks.delay(j.user,i.user)
        print "Sync Complete"



