from django.db import models
from django.contrib.auth.models import User
from  django.db.models.signals import post_save
from django.dispatch import receiver
from ..core.models import BaseMMModel


# Create your models here.

class MMcontact_name(BaseMMModel):
    name = models.CharField(('name'), max_length=30, blank=False)

@receiver(post_save, sender=MMcontact_name)
def check_for_MMcontact_name(sender, **kwargs):
    MMcontact_name.objects.all().delete()


class MMUser(BaseMMModel):
    user = models.OneToOneField(User, primary_key=True)
    name = models.CharField(('name'), max_length=30, blank=False)

    def get_primary(self):
        second = MMSecondaryUser.objects.get(secondary = self.user)
        if second:
            return second.primary

# class MMSecondaryUser(BaseMMModel):
#     primary = models.ForeignKey(User)
#     secondary = models.OneToOneField(User)

@receiver(post_save, sender=User)
def check_for_MMUser(sender, **kwargs):
    if len(MMUser.objects.filter(user=kwargs['instance'])) > 0:
        MMUser.objects.filter(user=kwargs['instance']).delete()
    MMUser.objects.create(user=kwargs['instance'], name = kwargs['instance'].username )
    return


class MMcontact(BaseMMModel):
    user = models.ForeignKey(User, related_name="user")
    contact = models.ForeignKey(User, related_name="contact")
    @staticmethod
    def create_entry(user_value, contact_value):
        MMcontact.objects.create(user=user_value, contact=contact_value)
        return

    @staticmethod
    def view_contact():
        return MMcontact.objects.all()

class MMconnectaccount(BaseMMModel):
    user = models.ForeignKey(User, related_name="Firstuser")
    contact = models.ForeignKey(User, related_name="otheraccount")
    approved = models.BooleanField(default=False)


@receiver(post_save, sender=MMcontact)
def update_contact(sender, **kwargs):
    if len(MMcontact.objects.filter(user=kwargs['instance'].user, contact=kwargs['instance'].contact)) > 1:
        MMcontact.objects.filter(user=kwargs['instance'].user, contact=kwargs['instance'].contact).delete()
        MMcontact.objects.create(user=kwargs['instance'].user, contact=kwargs['instance'].contact)
    if len(MMcontact.objects.filter(user=kwargs['instance'].contact, contact=kwargs['instance'].user)) > 0:
        return
    else:
        MMcontact.objects.create(user=kwargs['instance'].contact, contact=kwargs['instance'].user)

class MMmeeting(BaseMMModel):
    user = models.ForeignKey(User, related_name="meeting_host", null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.CharField(('Duration'), max_length=30, null=True)
    meeting_confirmed = models.BooleanField(default=False)
    meeting_name = models.CharField(('Meeting Name'), max_length=30, blank=False)
    description  = models.CharField(('Description'), max_length=3000, blank=True)

class MMmeetingparticipant(BaseMMModel):
    meeting = models.ForeignKey(MMmeeting)
    participant = models.ForeignKey(User)
    required = models.BooleanField(default=True)

    @staticmethod
    def create_entry(Meeting,Participant,Required):
        MMmeetingparticipant.objects.create(meeting=Meeting,participant=Participant,required=Required)
        return

@receiver(post_save,sender=MMmeeting)
def update_participant_for_meeting(sender,**kwargs):
    print "In post save for add parti"
    if MMmeetingparticipant.objects.filter(meeting_id=kwargs['instance'].id,participant_id=kwargs['instance'].user_id).count()>0:
        return
    else:
        MMmeetingparticipant.objects.create(meeting_id=kwargs['instance'].id,participant_id=kwargs['instance'].user_id,required=True)
        print "Participant added to the meeitng"

class MMnotification(BaseMMModel):
    user = models.ForeignKey(User, related_name="notification_user", null=True)
    meeting = models.ForeignKey(MMmeeting)
    read = models.BooleanField(default=True)


