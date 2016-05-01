from django.core.management.base import BaseCommand, CommandError
from meetme.users.models import User

class Command(BaseCommand):
    help = 'Creates a bunch of test users for testing'

    def handle(self, *args, **options):
        self.create_user_for_creds('mdamon','sindhubalu30@gmail.com','Matt','Damon','meetme')
        self.create_user_for_creds('pwalker','vidyaa2394@gmail.com','Paul','Walker','meetme')
        self.create_user_for_creds('eolsen','gowrikrishnakumar29@gmail.com','Elizabeth','Olsen','meetme')
        self.create_user_for_creds('mbellucci','dweepsikrishna@yahoo.com','Monica','Bellucci','meetme')
        self.stdout.write('Creation Complete')


    def create_user_for_creds(self,username,email,first_name,last_name,password):
        u=User.objects.create(username=username,email=email,first_name=first_name,last_name=last_name)
        u.set_password(password)
        u.save()
        s = "Created User %s",u.username
        print s

