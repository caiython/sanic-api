from sanic.config import Config as BaseConfig

class Config(BaseConfig):
    DB_PATH = "db.sqlite3"
