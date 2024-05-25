import traceback

from typing import Callable

from fastapi.responses import ORJSONResponse
from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from configs import CONFIG, logger


class CatchExceptMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, 
        request: Request,
        call_next: Callable
    ) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.info(f"{e}")
            traceback_str = traceback.format_exc()
            exception_err = {
                "msg":str(e), 
                "traceback": traceback_str, "error_type": type(e).__name__
            }
            if CONFIG.TRACEBACK_IN_EXCEPT_MIDDELWARE == False:
                exception_err.pop("traceback")
            return ORJSONResponse(
                content={"detail": exception_err},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )