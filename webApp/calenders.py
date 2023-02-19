from datetime import datetime, timedelta
from pytz import timezone
from pytz import timezone
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_credentials():
    # Try to load credentials from the token.json file
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def create_calendar_event(doctor, date,start_time):
    service = build('calendar', 'v3', credentials=get_credentials())

    start_datetime = datetime.combine(date, start_time)
    end_datetime = start_datetime + timedelta(minutes=45)
    timezone_str = 'America/New_York'  # Replace with the doctor's timezone
    timezone_obj = timezone(timezone_str)
    start_time_zone = timezone_obj.localize(start_datetime).isoformat()
    end_time_zone = timezone_obj.localize(end_datetime).isoformat()

    # Create event body
    start = {
        'datetime': start_time_zone,
        'timeZone': timezone_str,
    }
    end = {
        'dateTime': end_time_zone,
        'timeZone': timezone_str,
    }
    event = {
        'description': 'Appointment with Dr. ' + doctor.user.first_name + ' ' + doctor.user.last_name,
        'start': start,
        'end': end,
    }

    # Call the Calendar API to create the event
    calendar_id = doctor.calendar_id
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return event


