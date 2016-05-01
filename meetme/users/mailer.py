__author__ = 'hacker'
from django.core.mail import send_mail
from django.conf import settings
from django.template import Template,Context
from django.template.loader import get_template
# from ..settings import URL,UNSUB_LINK

class MeetmeMailer(object):

    def __init__(self):
        self.subject = ''
        self.from_email = settings.MEETME_FROM_EMAIL
        self.to_email = []
        self.template=''

    def send_email(self):
        for i in self.to_email:
            print i
            send_mail(self.subject,'',self.from_email,[i.email],fail_silently=True,html_message=self.render_template(i))
            print "Email has been sent to user "+i.username

    def render_template(self,user):
        t= get_template(self.template)
        c = Context(self.get_context_dict(user))
        return t.render(c)

    def get_context_dict(self,user):
        context = {}
        context['url'] = settings.URL
        context['unsub'] = settings.UNSUB_LINK
        return context


class MeetmeEventNotification(MeetmeMailer):

    def __init__(self,to_list,template_name,meeting):
        super(MeetmeEventNotification, self).__init__()
        self.subject = 'You have a new meeting invite'
        self.to_email = to_list
        self.template = template_name
        self.meeting = meeting

    def get_context_dict(self,user):
        context = super(MeetmeEventNotification, self).get_context_dict(user)
        context['name'] = user.get_full_name() or user.username
        context['id'] = user.username
        context['meeting'] = self.meeting
        context['host'] = self.meeting.user.get_full_name() or self.meeting.user.username
        return context


class MeetmeUserConnectNotification(MeetmeMailer):

    def __init__(self,to_list,template_name,connector,connectee):
        super(MeetmeUserConnectNotification, self).__init__()
        self.subject = 'You have a new connect request'
        self.to_email = to_list
        self.template = template_name
        self.connector = connector
        self.connectee = connectee

    def get_context_dict(self,user):
        context = super(MeetmeUserConnectNotification, self).get_context_dict(user)
        context['connector'] = self.connector
        context['connectee'] = user
        context['name'] = user.get_full_name() or user.username
        print context
        return context

class MeetingAbouttoStart(MeetmeEventNotification):

    def __init__(self,to_list,template_name,meeting):
        super(MeetmeEventNotification, self).__init__()
        self.subject = 'Your Meeting is about to start'
        self.to_email = to_list
        self.template = template_name
        self.meeting = meeting

    def get_context_dict(self,user):
        context = super(MeetingAbouttoStart, self).get_context_dict(user)
        context['meeting_datetime'] = self.meeting.start_time
        return context
