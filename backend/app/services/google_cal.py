import logging
from datetime import datetime, timedelta, timezone

from app.config import settings
from httpx import AsyncClient

logger = logging.getLogger(__name__)


def sanitize_keys(d: dict) -> dict:
    """Santize dict unnecessary dict keys"""
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
        return [sanitize_keys(v) for v in d]
    return {k: sanitize_keys(v) for k, v in d.items()
            if k not in remove_key}


class GoogleCal:
    """"Google Calendar Class"""

    def __init__(
            self,
            api_key: str,
            cal_id: str,
            tz_offset: int = 3,
            ignore_event_days: int = 1):

        self._setup(tz_offset=tz_offset, ignore_event_days=ignore_event_days)

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
            'timeMin': self.iso,
        }

        self.api_key = api_key
        self.cal_id = cal_id
        self.cal_url = f'https://clients6.google.com/calendar/v3/calendars/{cal_id}/events'
        self.last_response = None

    def _setup(self, tz_offset: int, ignore_event_days: int):
        """Setup timezone info

        Args:
            tz_offset (int): Time zone offset in hours from UTC
            ignore_event_days (int): Ignore events older than n days 
        """

        offset = timedelta(hours=tz_offset)
        tz = timezone(offset, name='МСК')
        yesterday = datetime.now(tz=tz) - timedelta(days=ignore_event_days)
        self.iso = yesterday.astimezone().isoformat()

    async def get(self, sanitize: bool = False) -> dict:
        """Get Google Calendar JSON"""

        async with AsyncClient() as client:
            response = await client.get(self.cal_url, params=self.params)
        response_json = response.json()
        events = response_json.get('items', [])

        elapsed = response.elapsed.total_seconds()
        slow_warning = elapsed > 0.7
        log_message = f'Response {response.status_code}, ' \
            f'time {elapsed:.4f}s, ' \
            f'events {len(events)}, ' \
            f'yesterday {self.iso}, '

        if response.status_code == 200 and not slow_warning:
            logger.info(log_message)
        elif slow_warning:
            logger.warning(log_message)
        else:
            logger.error(log_message)

        self.last_response = events

        if sanitize:
            sanitize_events = sanitize_keys(events)
            return sanitize_events
        return events


calendar = GoogleCal(api_key=settings.CAL_API_KEY,
                     cal_id=settings.CAL_ID)


# Service startup
async def start_calendar():
    logger.info('Google Calendar service startup BEGIN')
    events = await calendar.get(sanitize=True)
    logger.info(
        f'Google Calendar service startup DONE, Got {len(events)} events')


# Dependency
async def get_calendar() -> GoogleCal:
    yield calendar
