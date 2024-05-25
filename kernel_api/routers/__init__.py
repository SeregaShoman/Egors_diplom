from .auth import auth_router
from .events import event_router
from .static_servises import static_tags_router

available_routers = (
    auth_router, static_tags_router, event_router
)