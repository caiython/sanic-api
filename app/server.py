from sanic import Sanic
from sanic.response import text
from sanic_ext import Extend
from dotenv import load_dotenv
from mayim.extension import SanicMayimExtension

from app.config import Config
from app.listeners import setup_db
from app.blueprints import *
from app.executors import GameExecutor
from app.migrations import run_migrations


def create_app(config=Config) -> Sanic:
    load_dotenv()
    app = Sanic("MyHelloWorldApp", config())
    app.add_task(run_migrations())
    app.register_listener(setup_db, "before_server_start")
    app.blueprint(helloworld_bp)
    app.blueprint(game_bp)
    Extend.register(
        SanicMayimExtension(
            executors=[GameExecutor],
            dsn=app.config.DB_PATH,
        )
    )

    return app
