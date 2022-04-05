import logging
import time

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

        log_message = f'Request "{request.url.path}" ' \
            f'{response.status_code} time {process_time:.5f}s '

        slow_warning = process_time > self.time_warning
        if response.status_code < 203 and not slow_warning:
            logger.info(log_message)
        elif response.status_code < 500 or slow_warning:
            logger.warning(log_message)
        else:
            logger.error(log_message)

        return response
