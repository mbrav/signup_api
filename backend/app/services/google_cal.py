import json
import logging
from datetime import datetime, timedelta, timezone

from httpx import AsyncClient, Client

logger = logging.getLogger(__name__)

offset = timedelta(hours=3)
tz = timezone(offset, name='МСК')
yesterday = datetime.now(tz=tz) - timedelta(days=1)
iso = yesterday.astimezone().isoformat()


def remove_keys(d):
    """Remove unnecessary dict keys"""
    remove_key = [
        'accessRole',
        'defaultReminders',
        'kind',
        'etag',
        'status',
        'creator',
        'organizer',
        'sequence',
        'eventType',
    ]
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [remove_keys(v) for v in d]
    return {k: remove_keys(v) for k, v in d.items()
            if k not in remove_key}


class GoogleCal:
    """"Google Calendar Class"""

    def __init__(
            self,
            api_key: str,
            cal_id: str):

        self.params = {
            'calendarId': cal_id,
            'key': api_key,
            'singleEvents': 'true',
            'timeZone': 'Europe/Moscow',
            'maxAttendees': 1,
            'singleEvents': 'true',
            'maxResults': 250,
            'orderBy': 'startTime',
            'sanitizeHtml': 'true',
            'timeMin': iso,
        }

        self.api_key = api_key
        self.cal_id = cal_id
        self.cal_url = f'https://clients6.google.com/calendar/v3/calendars/{cal_id}/events'
        self.last_response = None

    def get(self):
        """Get Google Calendar JSON"""

        # async with httpx.AsyncClient() as client:
        #     response = client.get(self.cal_url, params=self.params)
        with Client() as client:
            response = client.get(self.cal_url, params=self.params)
        response_json = response.json()
        events = response_json.get('items', [])

        elapsed = response.elapsed.total_seconds()
        slow_warning = elapsed > 0.7
        log_message = f'Response {response.status_code}, ' \
            f'time {elapsed:.4f}s, ' \
            f'events {len(events)}, ' \
            f'yesterday {iso}, '

        if response.status_code == 200 and not slow_warning:
            logger.info(log_message)
        elif slow_warning:
            logger.warning(log_message)
        else:
            logger.error(log_message)

        clean = remove_keys(response_json)
        self.last_response = clean
        return clean


if __name__ == '__main__':
    cal = GoogleCal()
    res = cal.get()
    print(res)
