from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from pytz import timezone
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None
 
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_calendar_event(doctor, date, start_time):
    service = build('calendar', 'v3', credentials=get_credentials())

    start_datetime = datetime.combine(date, start_time)
    end_datetime = start_datetime + timedelta(minutes=45)

    timezone_str = 'Asia/Kolkata'
    timezone_obj = timezone(timezone_str)

    start_time_zone = timezone_obj.localize(start_datetime).isoformat()
    end_time_zone = timezone_obj.localize(end_datetime).isoformat()

    event = {
        'summary': 'Appointment',
        'description': 'Appointment with Dr. ' + doctor.user.first_name + ' ' + doctor.user.last_name,
        'start': {
            'dateTime': start_time_zone,
            'timeZone': timezone_str,
        },
        'end': {
            'dateTime': end_time_zone,
            'timeZone': timezone_str,
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    if event: return True
    else:return False
