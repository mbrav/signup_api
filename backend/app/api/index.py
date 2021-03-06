from datetime import datetime

from app.config import settings
from fastapi import APIRouter, Request

router = APIRouter()


@router.get(path='/')
async def health_check(request: Request, message: str = None):
    """API Health Check """

    response = {
        'status': 'OK',
        'response': 'Fast API service for signups and Telegram integration',
        'version': settings.VERSION,
        'client': request.client.host,
        'time': datetime.utcnow().isoformat()
    }
    return response
