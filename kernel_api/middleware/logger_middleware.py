from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from configs import logger, CONFIG


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, 
        request: Request,
        call_next: Callable
    ) -> Response:
        request_info = [
            ["Method", request.method], ["URL", request.url],
            ["Query Params", dict(request.query_params)],
            ["Path Params", dict(request.path_params)],
            ["Headers", dict(request.headers)], 
            ["Client", request.client],
        ]
        if CONFIG.LOG_LEVEL == "DEBUG":
            request_info.append(["Body", await request.body()])
        response = await call_next(request)
        logger.info(f"{request_info}")
        return response
        
            
