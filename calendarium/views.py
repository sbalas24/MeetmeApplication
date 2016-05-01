"""Views for the ``calendarium`` app."""
import calendar
from dateutil.relativedelta import relativedelta
from meetme.users.models import MMmeeting, MMmeetingparticipant

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.timezone import datetime, now, timedelta, utc
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    DetailView,
    RedirectView,
    TemplateView,
)

from .settings import SHIFT_WEEKSTART
from .utils import monday_of_week

class CalendariumRedirectView(RedirectView):
    """View to redirect to the current month view."""
    def get_redirect_url(self, **kwargs):
        return reverse('calendar_month', kwargs={'year': now().year,
                                                 'month': now().month})


class MonthView(TemplateView):
    """View to return all occurrences of an event for a whole month."""
    template_name = 'calendarium/calendar_month.html'
    model = MMmeeting

    def get_queryset(self):
        meeting_ids = [i.meeting.id for i in MMmeetingparticipant.objects.filter(participant_id=self.request.user.id)]
        return MMmeeting.objects.filter(id__in = meeting_ids)

    def dispatch(self, request, *args, **kwargs):
        self.month = int(kwargs.get('month'))
        self.year = int(kwargs.get('year'))
        if self.month not in range(1, 13):
            raise Http404
        if request.method == 'POST':
            if request.POST.get('next'):
                new_date = datetime(self.year, self.month, 1) + timedelta(
                    days=31)
                kwargs.update({'year': new_date.year, 'month': new_date.month})
                return HttpResponseRedirect(
                    reverse('calendar_month', kwargs=kwargs))
            elif request.POST.get('previous'):
                new_date = datetime(self.year, self.month, 1) - timedelta(
                    days=1)
                kwargs.update({'year': new_date.year, 'month': new_date.month})
                return HttpResponseRedirect(
                    reverse('calendar_month', kwargs=kwargs))
            elif request.POST.get('today'):
                kwargs.update({'year': now().year, 'month': now().month})
                return HttpResponseRedirect(
                    reverse('calendar_month', kwargs=kwargs))
        if request.is_ajax():
            self.template_name = 'calendarium/partials/calendar_month.html'
        return super(MonthView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        firstweekday = 0 + SHIFT_WEEKSTART
        while firstweekday < 0:
            firstweekday += 7
        while firstweekday > 6:
            firstweekday -= 7
        month = [[]]
        week = 0
        start = datetime(year=self.year, month=self.month, day=1, tzinfo=utc)
        end = datetime(
            year=self.year, month=self.month, day=1, tzinfo=utc
        ) + relativedelta(months=1)

        occurrences = []
        cal = calendar.Calendar()
        cal.setfirstweekday(firstweekday)
        all_occurrences = self.get_queryset().filter(start_time__month=self.month, start_time__year=self.year)
        print '------------'
        print all_occurrences
        for day in cal.itermonthdays(self.year, self.month):
            current = False
            if day:
                date = datetime(year=self.year, month=self.month, day=day,
                                tzinfo=utc)
                if date.date() == now().date():
                    current = True
            month[week].append((day, all_occurrences.filter(start_time__day=day), current))
            if len(month[week]) == 7:
                month.append([])
                week += 1
        calendar.setfirstweekday(firstweekday)
        weekdays = [_(header) for header in calendar.weekheader(10).split()]
        ctx = {'month': month, 'date': date, 'weekdays': weekdays}
        return ctx


class WeekView(TemplateView):
    """View to return all occurrences of an event for one week."""
    template_name = 'calendarium/calendar_week.html'
    model = MMmeeting

    def get_queryset(self):
        meeting_ids = [i.meeting.id for i in MMmeetingparticipant.objects.filter(participant_id=self.request.user.id)]
        return MMmeeting.objects.filter(id__in = meeting_ids)


    def dispatch(self, request, *args, **kwargs):
        self.week = int(kwargs.get('week'))
        self.year = int(kwargs.get('year'))
        if self.week not in range(1, 53):
            raise Http404
        if request.method == 'POST':
            if request.POST.get('next'):
                date = monday_of_week(self.year, self.week) + timedelta(days=7)
                kwargs.update(
                    {'year': date.year, 'week': date.date().isocalendar()[1]})
                return HttpResponseRedirect(
                    reverse('calendar_week', kwargs=kwargs))
            elif request.POST.get('previous'):
                date = monday_of_week(self.year, self.week) - timedelta(days=7)
                kwargs.update(
                    {'year': date.year, 'week': date.date().isocalendar()[1]})
                return HttpResponseRedirect(
                    reverse('calendar_week', kwargs=kwargs))
            elif request.POST.get('today'):
                kwargs.update({
                    'year': now().year,
                    'week': now().date().isocalendar()[1],
                })
                return HttpResponseRedirect(
                    reverse('calendar_week', kwargs=kwargs))
        if request.is_ajax():
            self.template_name = 'calendarium/partials/calendar_week.html'
        return super(WeekView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        date = monday_of_week(self.year, self.week) + relativedelta(
            days=SHIFT_WEEKSTART)
        week = []
        day = SHIFT_WEEKSTART
        start = date
        end = date + relativedelta(days=7 + SHIFT_WEEKSTART)
        while day < 7 + SHIFT_WEEKSTART:
            current = False
            if date.date() == now().date():
                current = True
            week.append((date, self.get_queryset().filter(start_time__day=date.day, start_time__month=date.month, start_time__year=self.year), current))
            day += 1
            date = date + timedelta(days=1)
        ctx = {'week': week, 'date': date, 'week_nr': self.week}
        return ctx


class DayView(TemplateView):
    """View to return all occurrences of an event for one day."""
    template_name = 'calendarium/calendar_day.html'
    model = MMmeeting

    def get_queryset(self):
        meeting_ids = [i.meeting.id for i in MMmeetingparticipant.objects.filter(participant_id=self.request.user.id)]
        return MMmeeting.objects.filter(id__in = meeting_ids)


    def dispatch(self, request, *args, **kwargs):
        self.day = int(kwargs.get('day'))
        self.month = int(kwargs.get('month'))
        self.year = int(kwargs.get('year'))
        try:
            self.date = datetime(year=self.year, month=self.month,
                                 day=self.day, tzinfo=utc)
        except ValueError:
            raise Http404
        if request.method == 'POST':
            if request.POST.get('next'):
                date = self.date + timedelta(days=1)
                kwargs.update(
                    {'year': date.year, 'month': date.month, 'day': date.day})
                return HttpResponseRedirect(
                    reverse('calendar_day', kwargs=kwargs))
            elif request.POST.get('previous'):
                date = self.date - timedelta(days=1)
                kwargs.update({
                    'year': date.year,
                    'month': date.month,
                    'day': date.day,
                })
                return HttpResponseRedirect(
                    reverse('calendar_day', kwargs=kwargs))
            elif request.POST.get('today'):
                kwargs.update({
                    'year': now().year,
                    'month': now().month,
                    'day': now().day,
                })
                return HttpResponseRedirect(
                    reverse('calendar_day', kwargs=kwargs))
        if request.is_ajax():
            self.template_name = 'calendarium/partials/calendar_day.html'
        return super(DayView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        print self.date.day
        occurrences = self.get_queryset().filter(start_time__day=self.date.day, start_time__month=self.month, start_time__year=self.year)
        ctx = {'date': self.date, 'occurrences': occurrences}
        print ctx
        return ctx


class EventDetailView(DetailView):
    """View to return information of an event."""
    model = MMmeeting


class EventMixin(object):
    """Mixin to handle event-related functions."""
    model = MMmeeting
    fields = '__all__'

    @method_decorator(permission_required('calendarium.add_event'))
    def dispatch(self, request, *args, **kwargs):
        return super(EventMixin, self).dispatch(request, *args, **kwargs)


