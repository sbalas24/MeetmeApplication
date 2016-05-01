import requests
from models import User
from social_auth.models import UserSocialAuth
from django.conf import settings
import json

def get_calender_for_user(user_id):
    u= User.objects.get(id=user_id)
    usocial_auth = UserSocialAuth.objects.get(user=u)
    headers = {}
    headers['Authorization'] = 'Bearer '+usocial_auth.tokens['access_token']
    print headers
    url = 'https://www.googleapis.com/calendar/v3/users/me/calendarList'
    r = requests.get(settings.GOOGLE_CALENDAR_EVENT_API,headers=headers)
    return json.loads(r.content)

