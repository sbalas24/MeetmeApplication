from django.shortcuts import render
from django.views.generic import View,TemplateView
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from ..users.tasks import get_calender_for_user, get_facebook_events , get_facebook_name
import json
from django.conf import settings
# Create your views here.


class IndexView(View):
    def get(self,request):
        if request.user.is_authenticated():
            print "Current user",request.user
            get_calender_for_user.delay(request.user.id)
            get_facebook_events.delay(request.user.id)
            get_facebook_name.delay(request.user.id)
            return HttpResponseRedirect(reverse('core:home'))
        return HttpResponseRedirect(reverse('users:login'))


class ApiView(View):
    def get(self,request):
        print request.META['HTTP_BATMAN']
        return HttpResponse(json.dumps({'jedi':'sith'}))

class CoreHome(TemplateView):
    template_name = 'core/home.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return HttpResponseRedirect('/login/')
        return super(CoreHome, self).get(request,*args,**kwargs)