from sanic.config import Config as BaseConfig
import os

class Config(BaseConfig):
    DB_PATH = os.getenv('SQLITE_DB_FPATH', 'db.sqlite3')
