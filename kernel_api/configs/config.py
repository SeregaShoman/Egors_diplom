from functools import cached_property
from pydantic_settings import BaseSettings


class Config(BaseSettings):

    TITLE: str = "API"
    UVICORN_LIMIT_MAX_REQUESTS: int = 100
    VERSION: str = "0.0.1"

    WORKERS_COUNT: int = 3
    BIND_ADDRESS: str
    LOG_LEVEL: str = "DEBUG"

    TRACEBACK_IN_EXCEPT_MIDDELWARE: bool
    ON_EXCEPT_MIDDELWARE: bool
    ON_LOGGER_MIDDELWARE: bool

    DRIVERNAME: str 
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str

    JWT_SECRET: str = "JWT_SECRET"
    
    @cached_property
    def get_app_config(self) -> dict[str, str | bool | None]:
        return {
            "title": self.TITLE, "version": self.VERSION
        }

CONFIG = Config()