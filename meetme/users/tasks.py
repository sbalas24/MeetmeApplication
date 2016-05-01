from __future__ import absolute_import
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
import requests
from .models import User,MMmeeting,MMmeetingparticipant,MMcontact,MMnotification
from social_auth.models import UserSocialAuth
from django.conf import settings
import json
from datetime import datetime,timedelta
from dateutil import parser
from .mailer import MeetmeEventNotification,MeetmeUserConnectNotification

@shared_task()
def get_calender_for_user(user_id):
    u= User.objects.get(id=user_id)
    usocial_auth = UserSocialAuth.objects.get(user=u)
    headers = {}
    headers['Authorization'] = 'Bearer '+usocial_auth.tokens['access_token']
    r = requests.get(settings.GOOGLE_CALENDAR_EVENT_API,headers=headers)
    events = json.loads(r.content)
    print "User "+u.username+" has"+str(len(events['items']))+" events"
    for event in events['items']:
        try:
            starttime = parser.parse(event['start']['dateTime'])
            endtime = parser.parse(event['end']['dateTime'])
            name = event['summary']
            duration = endtime-starttime
            duration=duration.total_seconds()/3600
            if not MMmeeting.objects.filter(start_time=starttime,user_id=user_id).count()>0:
                print "No prior meeting for "+u.username+" exists"
                MMmeeting.objects.create(start_time=starttime,user_id=user_id,end_time=endtime,meeting_name=name,meeting_confirmed=True,duration=duration)
        except Exception as e:
            print "There was an exception %s"%e
            continue
    print "user "+str(u.username)+"'s Google Calendar is now synced"


def get_facebook_email(token):
    params = {}
    params['access_token'] = token
    params['fields'] = 'id,name,email'
    r = requests.get(settings.FACEBOOK_USER_DATA_URL,params=params)
    return json.loads(r.content)



@shared_task()
def get_facebook_events(user_id):
    user = User.objects.get(id=user_id)
    params = {}
    params['access_token'] = user.facebookprofile.access_token
    params['fields'] = 'name,events{id,description,end_time,name,start_time}'
    r = requests.get(settings.FACEBOOK_USER_DATA_URL,params=params)
    print r.content
    events = json.loads(r.content)['events']['data']
    print "User "+user.username+" has"+str(len(events))+" events"
    for event in events:
        try:
            starttime = parser.parse(event['start_time'])
            try:
                endtime = parser.parse(event['end_time'])
            except:
                endtime = starttime + timedelta(hours=5)
            name = event['name']
            if endtime:
                duration = endtime-starttime
                duration=duration.total_seconds()/3600
            else:
                duration = None
            if not MMmeeting.objects.filter(start_time=starttime,user_id=user.id).count()>0:
                print "No prior meeting for "+user.username+" exists"
                MMmeeting.objects.create(start_time=starttime,user_id=user.id,end_time=endtime,meeting_name=name,meeting_confirmed=True,duration=duration)
        except Exception as e:
            print "There was an exception %s"%e
            continue
    name = json.loads(r.content)['name'].split()
    user.first_name = name[0]
    user.last_name = name[len(name)-1]
    user.save()
    print "user "+str(user.username)+"'s Facebook Calendar is now synced"

@shared_task()
def send_meeting_invite_email(meeting_id):
    M = MMmeeting.objects.get(id=meeting_id)
    participants = M.mmmeetingparticipant_set.exclude(participant_id=M.user_id).values_list('participant')
    participants = User.objects.filter(id__in=participants)
    print participants
    email_obj = MeetmeEventNotification(participants,'emails/meetinginvite.html',M)
    email_obj.send_email()

@shared_task()
def extract_and_tasks_for_user(primary,secondary):
    for i in MMmeetingparticipant.objects.filter(participant_id = secondary):
        if MMmeetingparticipant.objects.filter(participant_id=primary).count()>0:
            pass
        else:
            i.participant_id = primary
    print "Sync Complete"

@shared_task()
def send_user_connect_invite_email(connector,connectee):
    email_obj = MeetmeUserConnectNotification([connectee],'emails/user_connect.html',connector,connectee)
    email_obj.send_email()


@shared_task()
def sync_tasks(connector,connectee):
    for participant_row in MMmeetingparticipant.objects.filter(participant = connectee):
        if not MMmeetingparticipant.objects.filter(participant=connector,meeting=participant_row.meeting).count()>0:
            if not MMmeeting.objects.filter(start_time=participant_row.meeting.start_time,user_id=connector.id).count()>0:
                participant_row.participant = connector
                participant_row.save()
    for host_row in MMmeeting.objects.filter(user = connectee):
        if not MMmeeting.objects.filter(start_time=host_row.start_time,user_id=connector.id).count()>0:
            host_row.user = connector
            host_row.save()
    for contact_row in MMcontact.objects.filter(user = connectee):
        if not MMcontact.objects.filter(user = connector,contact = contact_row.contact).count()>0:
            contact_row.user = connector
            contact_row.save()
    for contact_row in MMcontact.objects.filter(contact = connectee):
        if not MMcontact.objects.filter(user = contact_row.user,contact = connector):
            contact_row.contact = connector
            contact_row.save()
    for notif_row in MMnotification.objects.filter(user = connectee):
        if not MMnotification.objects.filter(user = connector,meeting = notif_row.meeting).count()>0:
            notif_row.user = connector
            notif_row.save()
    print "Sync Complete"


@shared_task()
def get_facebook_name(user_id):
    u=User.objects.get(id=user_id)
    params = {}
    params['access_token'] = u.facebookprofile.access_token
    params['fields'] = 'id,name,email'
    r = requests.get(settings.FACEBOOK_USER_DATA_URL,params=params)
    name = json.loads(r.content)['name']
    name=name.split()
    u.first_name = name[0]
    u.last_name = name[-1]
    u.save()


@shared_task()
def meeting_about_to_start(meeting_id):
    M = MMmeeting.objects.get(id=meeting_id)
    participants = M.mmmeetingparticipant_set.exclude(participant_id=M.user_id).values_list('participant')
    participants = User.objects.filter(id__in=participants)
    print participants
    from .mailer import MeetingAbouttoStart
    email_obj = MeetingAbouttoStart(participants,'emails/abouttostart.html',M)
    email_obj.send_email()



