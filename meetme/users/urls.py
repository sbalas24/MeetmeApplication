__author__ = 'hacker'

from django.views.generic import TemplateView
from django.conf.urls import include,url
import views
import mailer

urlpatterns = [
    url(r'^register/$', views.UserCreateView.as_view(template_name='users/register.html'),name='register'),
    url(r'^login/$', views.UserLoginView.as_view(template_name='users/login.html'),name='login'),
    url(r'^logout/$', views.LogoutView.as_view(),name='logout'),
    url(r'^addContact/$', views.UserAddContactView.as_view(template_name='users/addContact.html'),name='addContact'),
    url(r'^view/$', views.UserContactview.as_view()),
    url(r'^meeting/$', views.MMMeetingAddView.as_view(template_name='users/meeting.html'),name='meeting'),
    url(r'^addParticipants/$', views.UserAddParticipantView.as_view(),name='addParticipants'),
    url(r'^editProfile/$', views.UserEditView.as_view(),name='editProfile'),
    url(r'^withdrawMeeting/$', views.UserwithdrawMeetingView.as_view(),name='withdrawMeeting'),
    url(r'^cancelMeeting/$', views.UsercancelMeetingView.as_view(),name='cancelMeeting'),
    url(r'^withdrawThisMeeting/$', views.UserwithdrawThisMeetingView.as_view(),name='withdrawThisMeeting'),
    url(r'^cancelThisMeeting/$', views.UsercancelThisMeetingView.as_view(),name='cancelThisMeeting'),
     url(r'^SpecificMeetingDetails/$', views.UserSpecificMeetingDetailsView.as_view(),name='SpecificMeetingDetails'),
    url(r'^declineMeeting/$', views.UserdeclineMeetingView.as_view(),name='declineMeeting'),
    url(r'^manageNotification/$', views.UsermanageNotificationView.as_view(),name='manageNotification'),
    url(r'^participants/$', views.UserParticipantView.as_view(),name='participants'),
    url(r'^meeting_time/$', views.UserSaveMeetingTimeView.as_view(),name='meeting_time'),
    url(r'^base/$', TemplateView.as_view(template_name='users/base2.html'),name='base'),
    url(r'^meetings/all/$', views.UserMeetingListView.as_view(),name='meetings_list'),
    url(r'^meetings/extract/$', views.UserExtractView.as_view(),name='meetings_extract'),
    url(r'^meetings/notifications/$', views.NotificationView.as_view(),name='notification'),
    url(r'^yo/$', TemplateView.as_view(template_name='core/home.html'),name='home'),
    url(r'^removed/$', TemplateView.as_view(template_name='users/removed.html'),name='removed'),
    url(r'^acceptMeeting/$', TemplateView.as_view(template_name='users/accepted.html'),name='acceptMeetin'),
    url(r'^connect/$', views.UserconnectaccountView.as_view(),name='connectacount'),
    url(r'^connectrequest/$', views.ConnectRequest.as_view(),name='connectrequest'),
    url(r'^error/$', TemplateView.as_view(template_name='users/errorpage.html'),name='error'),
    url(r'^tempf/$', views.TempFView.as_view(),name='f'),
]
