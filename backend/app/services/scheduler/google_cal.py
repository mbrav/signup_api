import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from app import db
from app.models import Event
from app.schemas import EventCalIn
from httpx import AsyncClient
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class EventListParams(BaseModel):
    key: str
    calendarId: str
    singleEvents: Optional[str] = 'true'
    timeZone: Optional[str] = 'Europe/Moscow'
    maxResults: Optional[int] = 250
    orderBy: Optional[str] = 'startTime'
    sanitizeHtml: Optional[str] = 'true'
    timeMin: Optional[str]
    # timeMax: Optional[datetime]


def sanitize_keys(d: dict) -> dict:
    """Sanitize dict unnecessary dict keys"""
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


def to_utc(date_string: datetime) -> datetime:
    return datetime.fromisoformat(date_string).astimezone(
        timezone.utc).replace(tzinfo=None)


class CalendarService:
    """"Google Calendar Class"""

    def __init__(
            self,
            api_key: str,
            cal_id: str,
            days_ago: int = 0):

        self.days_ago = days_ago
        self._set_time()
        self.params = EventListParams(
            key=api_key, calendarId=cal_id, timeMin=self.iso)
        self.cal_url = f'https://clients6.google.com/calendar/v3/calendars/{cal_id}/events'
        self.events = []

    def _set_time(self):
        """Setup event fetching time"""

        yesterday = datetime.utcnow() - timedelta(days=self.days_ago)
        self.iso = yesterday.astimezone().isoformat()

    async def fetch_events(self, sanitize: bool = False) -> List:
        """Fetch events from Google Calendar API"""

        async with AsyncClient() as client:
            response = await client.get(self.cal_url, params=self.params.dict())
        response_json = response.json()
        self.events = response_json.get('items', [])

        elapsed = response.elapsed.total_seconds()
        slow_warning = elapsed > 0.7
        log_message = f'Response {response.status_code}, ' \
            f'time {elapsed:.4f}s, ' \
            f'events {len(self.events)}, ' \
            f'yesterday {self.iso}, '

        if response.status_code == 200 and not slow_warning:
            logger.debug(log_message)
        elif slow_warning:
            logger.warning(log_message)
        else:
            logger.error(log_message)

    async def update_events(self):
        """Update events in db or create new ones"""

        self._set_time()
        await self.fetch_events()
        async with db.Session() as db_session:
            db_events = await self._get_events_db(db_session)
            await self._update_events_db(db_session, db_events)

    async def _get_events_db(self, db_session: AsyncSession) -> List[Event]:
        """Fetch events from database"""

        events = await Event.get_current(db_session)
        logger.debug(f'Got {len(events)} events from db')
        return events

    async def _update_events_db(
        self,
        db_session: AsyncSession,
        db_events: list[Event]
    ):
        """Create new events in db or create new ones"""
        event_db_dict = {event.google_id: event for event in db_events}

        for event in self.events:
            google_id = event['id']
            name = event['summary']
            description = event['description']
            start = to_utc(event['start']['dateTime'])
            end = to_utc(event['end']['dateTime'])
            google_modified = to_utc(
                event['updated'].replace('Z', '+00:00'))

            if google_id not in event_db_dict.keys():
                new_event = EventCalIn(
                    name=name,
                    description=description,
                    start=start,
                    end=end,
                    google_id=google_id,
                    google_modified=google_modified)

                new_object = Event(**new_event.dict())
                await new_object.save(db_session)
                logger.debug(
                    f'Added #{google_id} - {name} to db ')
                continue

            event = event_db_dict[google_id]

            name_changed = event.name != name
            desc_changed = False
            start_changed = event.start != start
            end_changed = event.end != end
            mod_changed = event.google_modified != google_modified

            changed = (name_changed or desc_changed
                       or start_changed or end_changed or mod_changed)
            if changed:
                event.name = name
                event.description = description
                event.start = start
                event.end = end
                event.google_modified = google_modified
                await event.update(db_session, **event.__dict__)
                logger.debug(
                    f'Updated #{google_id} - {name} in db ')
