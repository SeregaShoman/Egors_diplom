from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DRIVERNAME: str 
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str

    LOG_LEVEL: str = "DEBUG"

    WORK_INTERVAL: int


CONFIG = Config()