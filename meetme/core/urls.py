__author__ = 'hacker'

from django.views.generic import TemplateView
from django.conf.urls import include,url
import views

urlpatterns = [
    url(r'^home/$', views.CoreHome.as_view(),name='home'),
    url(r'^$', views.IndexView.as_view(),name='index'),
    url(r'^api/$', views.ApiView.as_view(),name='api'),
    ]
