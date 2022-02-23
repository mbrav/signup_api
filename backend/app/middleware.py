import json
import logging
import time

from httpx import AsyncClient
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Add request process time to response headers with logger"""

    time_warning = 0.2

    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = f'{process_time:.5f}'

        log_message = f'Request "{request.url.path}" {response.status_code}' \
            f'client {request.client.host} port {request.client.port} ' \
            f'time {process_time:.5f}s'

        slow_warning = process_time > self.time_warning
        if response.status_code < 203 and not slow_warning:
            logger.info(log_message)
        elif response.status_code < 500 or slow_warning:
            logger.warning(log_message)
        else:
            logger.error(log_message)

        return response


class ClientLookupMiddleware(BaseHTTPMiddleware):
    """Look up client info with logger"""

    def lookup(self, ip: str) -> str:
        return f'https://ipapi.co/{ip}/json/'

    async def dispatch(self, request, call_next):
        start_time = time.time()
        client_ip = request.client.host
        # client_ip = '8.8.8.8'
        async with AsyncClient() as client:
            response = await client.get(self.lookup(client_ip))

        process_time = time.time() - start_time

        res_json = response.json()
        ip = res_json['ip']
        country = res_json['country_name']
        city = res_json['city']
        region = res_json['region']
        timezone = res_json['timezone']
        organization = res_json['org']

        log_message = f'IP: "{ip}" Country: "{country}" Region: "{region}" ' \
            f'City: "{city}" Org: "{organization}" Timezone: "{timezone}" ' \
            f'Time {process_time:.5f}s'
        logger.info(log_message)

        response = await call_next(request)
        return response
