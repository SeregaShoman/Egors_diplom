from uvicorn.workers import UvicornWorker

from configs import CONFIG, logger

class MyUvicornWorker(UvicornWorker):
    logger = logger
    CONFIG_KWARGS = {
        "loop": "asyncio",
        "http": "httptools",
    }
    max_requests = CONFIG.UVICORN_LIMIT_MAX_REQUESTS
    if max_requests > 0: 
        CONFIG_KWARGS['limit_max_requests'] = max_requests

