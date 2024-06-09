from .auth import auth_router
from .events import event_router
from .tags import static_tags_router
from .users import users_router

available_routers = (
    auth_router, static_tags_router, event_router, users_router
)