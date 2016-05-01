from django.shortcuts import render_to_response
from django.views.generic import CreateView, FormView, View, ListView, TemplateView
from django.contrib.auth.models import User
from models import MMcontact, MMmeetingparticipant, MMmeeting, MMnotification, MMconnectaccount
from forms import MMUserCreationForm, MMUserLoginForm, MMUserAddContactForm, MMAddMeetingParticipant, \
    MMMeetingCreationForm, MMUserconnectaccountForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from dateutil import parser
from django.template.context import Context
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .forms import TempForm
# Create your views here.

class UserCreateView(CreateView):
    model = User
    form_class = MMUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('core:index')

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return super(UserCreateView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('core:index'))

    def get_success_url(self):
        if self.object:
            form = self.get_form()
            if form.is_valid():
                user = authenticate(username=self.object.username, password=form.cleaned_data['password'])
                print "User is", user
                login(self.request, user)
        return self.success_url


class UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = MMUserLoginForm
    success_url = reverse_lazy('core:index')

    def form_invalid(self, form):
        print "Form is invalid"
        print form.errors
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        if form.is_valid():
            u = User.objects.filter(username=form.cleaned_data['username'])
            print "User name",u
            if len(u) is 0:
                message ="Please, Create an account first"
                c = Context({'message': message})
                return render_to_response('users/errorpage.html', c)
            try:
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                login(self.request, user)
            except:
                message = "Invalid credentials"
                c = Context({'message': message})
                return render_to_response('users/errorpage.html', c)
        else:
            print "Login form not valid"
        return super(UserLoginView, self).form_valid(form)




class LogoutView(View):
    def get(self, request):
        print request.user
        if request.user.is_authenticated():
            logout(request)
        return HttpResponseRedirect(reverse('users:login'))


class UserContactview(FormView):
    def get(self, request, *args, **kwargs):


        print request.user.id


        s = ""
        name_list = []
        for i in MMcontact.objects.all():
            if i.user_id == request.user.id:
                s += str(User.objects.get(id=i.contact_id).first_name) + "\n"
                s += str(User.objects.get(id=i.contact_id).last_name) + "\n"
                name_list.append(s)
                s = ""
        html = "<html><body> The contacts are %s </body></html>" % (s)
        c = Context({'names': name_list})
        return render_to_response('users/viewcontacts.html', c)


class UserAddContactView(CreateView):
    template_name = 'users/addContact.html'
    form_class = MMUserAddContactForm
    success_url = reverse_lazy('core:home')
    
    def post(self, request, *args, **kwargs):
        super(UserAddContactView, self).post(request,*args,**kwargs)
        print self.success_url,"Success URL"
        if 'error' in self.success_url:
            print "Error redirecting"
            c = {}
            c['message'] = 'No such meetme user exists'
            return render_to_response('users/errorpage.html', c)
        return super(UserAddContactView, self).post(request,*args,**kwargs)


    
    def get_success_url(self):
        if self.object:
            form = self.get_form()
            if form.is_valid():
                try:
                    user = User.objects.get(id=self.request.user.id)
                    contact = User.objects.get(username=form.cleaned_data['name'])
                    MMcontact.create_entry(user, contact)
                except:
                    self.success_url =  '/error/'
        return self.success_url


class UserconnectaccountView(FormView):
    template_name = 'users/connect.html'
    form_class = MMUserconnectaccountForm
    success_url = reverse_lazy('core:home')

    def post(self, request, *args, **kwargs):
        super(UserconnectaccountView, self).post(request,*args,**kwargs)
        print self.success_url,"Success URL"
        if 'error' in self.success_url:
            print "Error redirecting"
            c = {}
            c['message'] = 'No such profile exists'
            return render_to_response('users/errorpage.html', c)
        return HttpResponseRedirect(self.success_url)

    def get_success_url(self):
        print "IN get success url"
        form = self.get_form()
        if form.is_valid():
            print "Form is valid"
            try:
                user = User.objects.get(id=self.request.user.id)
                contact = User.objects.get(username=form.cleaned_data['name'])
                print "GOnna Create User Now"
                MMconnectaccount.objects.create(user = user , contact = contact, approved = False)
                from .tasks import send_user_connect_invite_email
                send_user_connect_invite_email.delay(user,contact)
            except Exception as e:
                print "UserconnectaccountView %s"%e
                self.success_url =  '/error/'
        return self.success_url



class MMMeetingAddView(FormView):
    template_name = 'users/meeting.html'
    form_class = MMMeetingCreationForm
    success_url = reverse_lazy('users:participants')

    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        import pytz
        dict = {}
        print "Current user"
        dict['start_time'] = parser.parse(form.cleaned_data['starting_date'] + ' ' + form.cleaned_data['starting_time'])
        dict['start_time'] = dict['start_time'].replace(tzinfo=pytz.UTC)
        dict['end_time'] = parser.parse(form.cleaned_data['ending_date'] + ' ' + form.cleaned_data['ending_time'])
        dict['end_time'] = dict['end_time'].replace(tzinfo=pytz.UTC)
        dict['meeting_name'] = form.cleaned_data['meeting_name']
        dict['duration'] = str(form.cleaned_data['duration'])
        print dict['duration']
        dur_array = dict['duration'].split(':')
        duration = timedelta(hours=int(dur_array[0]), minutes=int(dur_array[1]))
        if dict['end_time'] < dict['start_time']:
            message = "End time cannot be less than start time"
            print message
            c = Context({'message': message})
            return render_to_response('users/errorpage.html', c)
        if duration > dict['end_time'] - dict['start_time']:
            message = "The time interval must be greater than the duration"
            print message
            c = Context({'message': message})
            return render_to_response('users/errorpage.html', c)
        dict['description'] = str(form.cleaned_data['description'])
        dict['user_id'] = self.request.user.id
        print dict
        if not MMmeeting.objects.filter(user_id=self.request.user.id, start_time=dict['start_time']).count() > 0:
            print "Gonn create meeting now"
            m = MMmeeting.objects.create(**dict)
            print "New meeting created", m.id
        return super(MMMeetingAddView, self).form_valid(form)

        # def get_success_url(self):
        #     if self.object:
        #         print "Inside get_success_url"
        #     print self.request.user.id
        #     self.object.user_id = self.request.user.id
        #     self.object.save()
        #     return self.success_url


class UserParticipantView(FormView):
    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        print "Adding participants"
        participants = self.get_queryset()
        meetings = self.getMeetings()
        c = Context({'participant': participants, 'meetings': meetings})
        return render_to_response('users/addParticipant.html', c)

    def get_queryset(self):
        contacts = MMcontact.objects.filter(user_id=self.request.user.id)
        participantlist = [None] * len(contacts)
        j = 0
        for i in contacts:
            s = User.objects.get(id=i.contact_id)
            participantlist[j] = s
            j += 1
        return participantlist

    def getMeetings(self):
        meetings = MMmeeting.objects.filter(user_id=self.request.user.id)
        return meetings

class UserEditView(TemplateView):


     def get(self, request, *args, **kwargs):
         user =User.objects.get(id = request.user.id)
         print user
         User_name = user.username
         last_name = user.last_name
         first_name = user.first_name

         id_name =  user.id
         email =   user.email
         c = Context({'uname': User_name, 'lname': last_name, 'fname': first_name, 'userid': id_name, 'email': email})

         if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
         if str(request).find("username") is -1:
            return render_to_response('users/editProfile.html', c)
         else:
              t = User.objects.get(id=request.user.id)
              t.first_name = request.GET.get('first_name')
              t.last_name = request.GET.get('last_name')
              t.email = request.GET.get('email')
              t.username = request.GET.get('username')
              t.save()
              return HttpResponseRedirect(reverse('core:home'))








class UserAddParticipantView(CreateView):
    template_name = 'users/addParticipant.html'
    model = MMmeetingparticipant
    form_class = MMAddMeetingParticipant

    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        meeting = MMmeeting.objects.get(id=request.GET['meeting'])
        req_participants = request.GET.getlist('req_participant')
        opt_participants = request.GET.getlist('opt_participant')
        for participant in req_participants:
            meeting_participant = MMmeetingparticipant.objects.filter(meeting = meeting, participant =User.objects.get(id = participant))
            if len(meeting_participant) > 0:
                meeting_participant[0].required = True
                meeting_participant[0].save()
            else:
                MMmeetingparticipant.create_entry(meeting, User.objects.get(id = participant), True)
        for participant in opt_participants:
            meeting_participant = MMmeetingparticipant.objects.filter(meeting = meeting, participant =User.objects.get(id = participant))
            if len(meeting_participant) > 0:
                meeting_participant[0].required = False
                meeting_participant[0].save()
            else:
                MMmeetingparticipant.create_entry(meeting, User.objects.get(id = participant), False)

        from .tasks import send_meeting_invite_email,meeting_about_to_start
        send_meeting_invite_email(meeting.id)
        import datetime
        a = meeting.start_time- datetime.timedelta(minutes=5)
        b=datetime.datetime.utcfromtimestamp(float(a.strftime('%s')))
        # print "Meeting Sceduled for",b
        # meeting_about_to_start.apply_async(args=[meeting.id], eta=(b))

        if meeting.meeting_confirmed == 1:
            return HttpResponseRedirect(reverse('core:home'))

        meeting_stime = meeting.start_time
        meeting_etime = meeting.end_time
        print "Meeting start time ,end time and duration"
        minutes_30 = timedelta(minutes=30)
        dur_array = meeting.duration.split(':')
        duration = timedelta(hours=int(dur_array[0]), minutes=int(dur_array[1]))
        print meeting_stime, meeting_etime, (meeting_etime - meeting_stime) + minutes_30
        first_name = User.objects.get(id=self.request.user.id).first_name
        last_name = User.objects.get(id=self.request.user.id).last_name
        name_s = last_name + "," + first_name
        req_participants.append(self.request.user.id)
        opt_participants.extend(req_participants)
        tent_stime = meeting.start_time
        number_of_meetings = 0
        possible_meeting_times = []
        possible_meeting_times_morning = []
        possible_meeting_times_afternoon = []
        possible_meeting_times_evening = []
        possible_meeting_times_night = []
        while tent_stime + duration <= meeting.end_time and (len(possible_meeting_times_morning)<=2
                                                            or len(possible_meeting_times_afternoon)<=2
                                                            or len(possible_meeting_times_evening)<=2
                                                            or len(possible_meeting_times_night)<=2):
            time_ok = True
            for participant in opt_participants:
                pid = User.objects.get(id = participant)
                meeting_ids = MMmeetingparticipant.objects.filter(participant_id=pid)
                print "The length of partcipants table is :"
                print len(meeting_ids)

                for mid in meeting_ids:
                    print "Meeting id:"
                    print mid.meeting_id
                    mmmeeting_list = MMmeeting.objects.filter(id=mid.meeting_id, meeting_confirmed=1)
                    if len(mmmeeting_list) == 0:
                        continue
                    mmmeeting = mmmeeting_list[0]
                    print "meeting Details: start_time, end_time"
                    print tent_stime, duration, mmmeeting.start_time, mmmeeting.end_time
                    if mmmeeting.end_time <= tent_stime or mmmeeting.start_time >= tent_stime+duration:
                        print "Yay the meeting time is not conflicting"
                        print tent_stime
                        time_ok = True
                        continue
                    if tent_stime < mmmeeting.end_time and tent_stime >= mmmeeting.start_time:
                        print "Not well1"
                        time_ok = False
                        break
                    elif tent_stime + duration <= mmmeeting.end_time and tent_stime + duration > mmmeeting.start_time:
                        print "Not well2"
                        time_ok = False
                        break
                    elif tent_stime <= mmmeeting.start_time and tent_stime + duration >= mmmeeting.end_time:
                        print "Not well 2"
                        time_ok = False
                        break
                    else:
                        print "All is well"
                        time_ok = True

                if time_ok is False:
                    break
            if time_ok is True:
                if tent_stime.hour >= 8 and tent_stime.hour < 12 and len(possible_meeting_times_morning) < 2:
                    possible_meeting_times_morning.append(tent_stime)
                elif tent_stime.hour >= 12 and tent_stime.hour < 16 and len(possible_meeting_times_afternoon) < 2:
                    possible_meeting_times_afternoon.append(tent_stime)
                elif tent_stime.hour >= 16 and tent_stime.hour < 20 and len(possible_meeting_times_evening) < 2:
                    possible_meeting_times_evening.append(tent_stime)
                else:
                    if len(possible_meeting_times_night) < 2:
                        possible_meeting_times_night.append(tent_stime)
                number_of_meetings += 1
                tent_stime += duration
            else:
                tent_stime += minutes_30
        possible_meeting_times.extend(possible_meeting_times_morning)
        possible_meeting_times.extend(possible_meeting_times_afternoon)
        possible_meeting_times.extend(possible_meeting_times_evening)
        possible_meeting_times.extend(possible_meeting_times_night)
        print possible_meeting_times
        if len(possible_meeting_times) -len(possible_meeting_times_night) > 0:
            message = "Congrats. Meeting times are available including all the participants"
            c = Context({'meeting_time': possible_meeting_times,'meeting': meeting, 'message': message})
            return render_to_response('users/meeting_time.html', c)
        tent_stime = meeting.start_time
        number_of_meetings = 0
        possible_meeting_times_optional = []
        possible_meeting_times_morning = []
        possible_meeting_times_afternoon = []
        possible_meeting_times_evening = []

        while tent_stime + duration <= meeting.end_time and (len(possible_meeting_times_morning)<=2
                                                            or len(possible_meeting_times_afternoon)<=2
                                                            or len(possible_meeting_times_evening)<=2
                                                            or len(possible_meeting_times_night)<=2):
            time_ok = True
            for participant in req_participants:
                pid = User.objects.get(id = participant)
                meeting_ids = MMmeetingparticipant.objects.filter(participant_id=pid)
                print "The length of partcipants table is :"
                print len(meeting_ids)

                for mid in meeting_ids:
                    print "Meeting id:"
                    print mid.meeting_id
                    mmmeeting_list = MMmeeting.objects.filter(id=mid.meeting_id, meeting_confirmed=1)
                    if len(mmmeeting_list) == 0:
                        continue
                    mmmeeting = mmmeeting_list[0]
                    print "meeting Details: start_time, end_time"
                    print tent_stime, duration, mmmeeting.start_time, mmmeeting.end_time
                    if mmmeeting.end_time <= tent_stime or mmmeeting.start_time >= tent_stime+duration:
                        print "Yay"
                        time_ok = True
                        continue
                    if tent_stime < mmmeeting.end_time and tent_stime >= mmmeeting.start_time:
                        time_ok = False
                        break
                    elif tent_stime + duration <= mmmeeting.end_time and tent_stime + duration > mmmeeting.start_time:
                        time_ok = False
                        break
                    elif tent_stime <= mmmeeting.start_time and tent_stime + duration >= mmmeeting.end_time:
                        time_ok = False
                        break
                    else:
                        time_ok = True

                if time_ok is False:
                    break
            if time_ok is True:
                if tent_stime.hour >= 8 and tent_stime.hour < 12 and len(possible_meeting_times_morning) < 2:
                    possible_meeting_times_morning.append(tent_stime)
                elif tent_stime.hour >= 12 and tent_stime.hour < 16 and len(possible_meeting_times_afternoon) < 2:
                    possible_meeting_times_afternoon.append(tent_stime)
                elif tent_stime.hour >= 16 and tent_stime.hour < 20 and len(possible_meeting_times_evening) < 2:
                    possible_meeting_times_evening.append(tent_stime)
                else:
                    if len(possible_meeting_times_night) < 2:
                        possible_meeting_times_night.append(tent_stime)
                number_of_meetings += 1
                tent_stime += duration
            else:
                tent_stime += minutes_30
        possible_meeting_times_optional.extend(possible_meeting_times_morning)
        possible_meeting_times_optional.extend(possible_meeting_times_afternoon)
        possible_meeting_times_optional.extend(possible_meeting_times_evening)
        possible_meeting_times_optional.extend(possible_meeting_times_night)
        print possible_meeting_times_optional
        if len(possible_meeting_times_optional) == 0:
            if len(possible_meeting_times) == 0:
                message = "There is no common meeting time for these participants. Please Try a different time"
                print message
                c = Context({'message': message})
                return render_to_response('users/errorpage.html', c)

        message = "Atleast on of the optional participant doesn't have a common meeting time."
        c = Context({'meeting_time': possible_meeting_times_optional,'meeting': meeting, 'message': message})
        return render_to_response('users/meeting_time.html', c)

class UserMeetingListView(ListView):
    model = MMmeeting
    template_name = 'users/meetings_list.html'
    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        meeting = self.get_queryset()
        print meeting
        c = Context({'meeting': meeting})
        return render_to_response('users/meetings_list.html', c)

    def get_queryset(self):
        meeting_ids = [i.meeting.id for i in MMmeetingparticipant.objects.filter(participant_id=self.request.user.id)]
        return MMmeeting.objects.filter(id__in = meeting_ids)



class UserwithdrawMeetingView(TemplateView):
    template_name = 'users/withdrawMeeting.html'
    model = MMmeeting
    success_url = reverse_lazy('core:home')
    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        meeting = self.get_queryset()
        print meeting
        c = Context({'meeting': meeting})

        if str(request).find("unique") is -1:
            return render_to_response('users/withdrawMeeting.html', c)
        else:
            MMmeetingparticipant.objects.filter(participant_id = self.request.user.id,meeting_id = self.request.GET['unique_cancel']).delete()
            return HttpResponseRedirect(reverse('core:home'))

    def get_queryset(self):
        meeting_ids = [i.meeting.id for i in MMmeetingparticipant.objects.filter(participant_id=self.request.user.id)]
        return MMmeeting.objects.filter(id__in = meeting_ids)

class UserdeclineMeetingView(TemplateView):
    template_name = 'emails/meetinginvite.html'
    model = MMmeetingparticipant
    def get(self, request, *args, **kwargs):
        participant = User.objects.filter(username = self.request.GET['id'])
        MMmeetingparticipant.objects.filter(participant = participant,meeting_id = self.request.GET['meeting_id']).delete()
        return HttpResponseRedirect(reverse('users:removed'))

class UsercancelMeetingView(TemplateView):
    template_name = 'users/cancelMeeting.html'
    model = MMmeeting
    success_url = reverse_lazy('core:home')
    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        meeting = self.get_queryset()
        print meeting
        c = Context({'meeting': meeting})

        if str(request).find("unique") is -1:
            return render_to_response('users/cancelMeeting.html', c)
        else:
            MMmeeting.objects.filter(user_id = self.request.user.id,id = self.request.GET['unique_cancel']).delete()
            MMmeetingparticipant.objects.filter(participant_id = self.request.user.id,meeting_id = self.request.GET['unique_cancel']).delete()
            return HttpResponseRedirect(reverse('users/cancelMeeting.html'))

    def get_queryset(self):
        return MMmeeting.objects.filter(user_id = self.request.user.id)

class UserwithdrawThisMeetingView(TemplateView):
    template_name = 'users/SpecificMeetingDetails.html'
    model = MMmeeting
    success_url = reverse_lazy('core:home')
    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        MMmeetingparticipant.objects.filter(participant_id = self.request.user.id,meeting_id = self.request.GET['meetingid']).delete()
        return HttpResponseRedirect(reverse('core:home'))

class UsermanageNotificationView(TemplateView):
    def get(self, request):

        uid = self.request.user.id
        Uname = str(User.objects.get(id=uid).username)

        if str(request).find("meetname") is -1:
            NotificationName = request.GET.get('Notname')
            c = Context ({'Notificname': NotificationName,'username' : Uname})

            return render_to_response('users/manageNotification.html', c)
        else:
            Meetid = MMmeeting.objects.get(meeting_name= self.request.GET['meetname']).id
            ch = str(self.request.GET['choice'])
            x = "Accept"
            y = "Decline"

            if ch == y:
                MMmeetingparticipant.objects.filter(participant_id = uid,meeting_id = Meetid).delete()
                MMnotification.objects.filter(user_id = uid,meeting_id = Meetid).delete()
                return HttpResponseRedirect(reverse('core:home'))
            elif ch == x:
                MMnotification.objects.filter(user_id = uid,meeting_id = Meetid).delete()
                return HttpResponseRedirect(reverse('core:home'))

class UsercancelThisMeetingView(TemplateView):
    template_name = 'users/SpecificMeetingDetails.html'
    model = MMmeeting
    success_url = reverse_lazy('core:home')
    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        MMmeeting.objects.filter(user_id = self.request.user.id,id = self.request.GET['meetingid']).delete()
        MMmeetingparticipant.objects.filter(participant_id = self.request.user.id,meeting_id = self.request.GET['meetingid']).delete()
        return HttpResponseRedirect(reverse('core:home'))


class UserSpecificMeetingDetailsView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        mname = self.request.GET.get('mname')
        meeting = MMmeeting.objects.get(id= mname)

        host_id = meeting.user_id
        host_name = str(User.objects.get(id=host_id).last_name)
        host_name += ","
        host_name += str(User.objects.get(id=host_id).first_name)
        meetid = meeting.id
        contacts = MMmeetingparticipant.objects.filter(meeting_id = meetid)
        participantlist = [None] * len(contacts)
        j = 0
        for i in contacts:
            s = ""
            s += str(User.objects.get(id=i.participant_id).last_name) + ","
            s += str(User.objects.get(id=i.participant_id).first_name)
            participantlist[j] = s
            j += 1
        if meeting.user_id == request.user.id:
            url = "cancelThisMeeting"
            label = "Cancel"
        else:
            url = "withdrawThisMeeting"
            label = "Withdraw"
        c = Context({'name': meeting,'host':host_name,'participants':participantlist, 'url': url, 'label': label})
        return render_to_response('users/SpecificMeetingDetails.html', c)


class UserSaveMeetingTimeView(CreateView):
    success_url = reverse_lazy('core:home')
    template_name = 'meeting_time'

    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        print request.GET['meetingtime']
        string = parser.parse(request.GET['meetingtime'])
        print request.GET['meet']
        meeting = MMmeeting.objects.get(id=request.GET['meet'])
        meeting.start_time = string
        dur_array = meeting.duration.split(':')
        duration = timedelta(hours=int(dur_array[0]), minutes=int(dur_array[1]))
        meeting.end_time = string + duration
        meeting.meeting_confirmed = 1
        meeting.save()
        participants = MMmeetingparticipant.objects.filter(meeting_id = meeting.id)
        print participants
        for mmuser in participants:
            MMnotification.objects.create(user = User.objects.get(id = mmuser.participant_id),meeting = meeting, read = False)
        return HttpResponseRedirect(reverse('core:home'))

class NotificationView(ListView):
    model = MMnotification
    template_name = 'users/viewnotification.html'
    success_url = reverse_lazy('core:home')

    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        return MMnotification.objects.filter(user_id = self.request.user.id)

    def post(self, request, *args, **kwargs):
        if(MMnotification.objects.filter(user_id = self.request.user.id)):
            notifications = MMnotification.objects.filter(user_id = self.request.user.id)
            for notif in notifications:
                notif.delete()
        return HttpResponseRedirect(reverse('core:home'))

# class UserConnectView(View):
#     def get(self,request,*args,**kwargs):
#         from .models import MMSecondaryUser
#         user_id = request.GET['primary']
#         if MMSecondaryUser.objects.filter(primary__id=request.user.id).count()>0:
#             pass
#         elif MMSecondaryUser.objects.filter(secondary__id=request.user.id).count()>0:
#             logout(request)
#             login(request,MMSecondaryUser.objects.get(secondary__id=request.user.id).primary)
#         else:
#             MMSecondaryUser.objects.create(primary__id = int(user_id),secondary__id=request.user.id)
#             logout(request)
#             login(request,User.objects.get(id=int(user_id)))
#         return HttpResponseRedirect(reverse('core:home'))

class UserExtractView(View):
    def get(self,request,*args,**kwargs):
        if request.user.id is None:
            return HttpResponseRedirect(reverse('users:login'))
        print "Current User",request.user,request.GET
        try:
            from .tasks import extract_and_tasks_for_user
            user_id = request.GET['primary']
            print  "Primary",user_id
            extract_and_tasks_for_user.delay(user_id,request.user.id)
            logout(request)
            login(request,User.objects.get(id=int(user_id)))
        except Exception as e:
            print e
            return HttpResponseRedirect(reverse("core:home"))


class ConnectRequest(View):
    def get(self,request,*args,**kwargs):
        try:
            connector = User.objects.get(id=int(request.GET['connector']))
            connectee = User.objects.get(id=int(request.GET['connectee']))
            m=MMconnectaccount.objects.get(user = connector , contact = connectee)
            m.approved = True
            m.save()
            """
            for participant_row in MMmeetingparticipant.objects.filter(participant = connectee):
                participant_row.participant = connector
                participant_row.save()
            for host_row in MMmeeting.objects.filter(user = connectee):
                host_row.user = connector
                host_row.save()
            for contact_row in MMcontact.objects.filter(user = connectee):
                contact_row.user = connector
                contact_row.save()
            for contact_row in MMcontact.objects.filter(contact = connectee):
                contact_row.contact = connector
                contact_row.save()
            for notif_row in MMnotification.objects.filter(user = connectee):
                notif_row.user = connector
                notif_row.save()
            """
            from .tasks import sync_tasks
            sync_tasks.delay(connector,connectee)
            print "connected"
        except Exception as e:
            print "Exception %s"%e
        return HttpResponseRedirect(reverse('core:home'))
    
class TempFView(FormView):
    form_class = TempForm
    success_url = reverse_lazy('core:index')
    template_name = 'users/tempf.html'

    def get_success_url(self):
        print "IN get success url"
        form = self.get_form()
        if form.is_valid():
            print "Form is valid"
            try:
                txt = form.cleaned_data['txt']
                print "GOnna print txt"
                print txt
            except Exception as e: print "%s"%e
        return super(TempFView, self).get_success_url()
                


