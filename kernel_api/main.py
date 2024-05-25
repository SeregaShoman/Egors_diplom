from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import available_routers
from configs import CONFIG, logger
from middleware import LoggingMiddleware, CatchExceptMiddleware


app = FastAPI(**CONFIG.get_app_config)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if CONFIG.ON_LOGGER_MIDDELWARE:
    app.add_middleware(LoggingMiddleware)


if CONFIG.ON_EXCEPT_MIDDELWARE:
    app.add_middleware(CatchExceptMiddleware)


async def on_startup():
    logger.info("The application has started running.")
    for router in available_routers:    
        logger.info(
            f"A router with the tag was registered: {router.tags[0]}"
        )
        app.include_router(router)

        
app.add_event_handler("startup", on_startup)
