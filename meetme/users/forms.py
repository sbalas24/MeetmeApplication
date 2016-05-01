

__author__ = 'hacker'

from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from models import MMcontact, MMcontact_name, MMmeeting,MMmeetingparticipant, MMconnectaccount
from django.contrib.admin import widgets
from datetimewidget.widgets import DateTimeWidget

class MMUserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super(MMUserCreationForm, self).save(False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


# class MMUserLoginForm(forms.Form):
#     class Meta:
#         model = User
#         fields = ['username','password']

class MMUserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    # class Meta:
    #     model = User
    #     fields = ['username','password']


class MMUserAddContactForm(ModelForm):
    class Meta:
        model = MMcontact_name
        fields = ['name']

class MMUserconnectaccountForm(ModelForm):
    class Meta:
        model = MMcontact_name
        fields = ['name']


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'


class MMMeetingCreate(ModelForm):
    duration = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),help_text='HH:MM')

    class Meta:
        model = MMmeeting
        fields = ['meeting_name', 'description',  'duration']
        # widgets = {
        #     'start_time': DateInput() ,
        #     'end_time': TimeInput(),
        # }

class MMMeetingCreationForm(forms.Form):
    starting_date = forms.CharField(widget=DateInput())
    starting_time = forms.CharField(widget=TimeInput())
    ending_date = forms.CharField(widget=DateInput())
    ending_time = forms.CharField(widget=TimeInput())
    meeting_name = forms.CharField()
    description = forms.CharField()
    #duration = forms.DurationField()
    duration=forms.TimeField(widget=forms.TimeInput(format='%H:%M'),help_text='HH:MM')

class MMAddMeetingParticipant(ModelForm):
    class Meta:
        model = MMmeetingparticipant
        fields = ['meeting','participant','required']

class TempForm(forms.Form):
    txt = forms.Textarea()

