from sanic import Sanic
from sanic.response import text
from dotenv import load_dotenv

from app.config import Config
from app.listeners import setup_db
from app.blueprints import helloworld_bp

def create_app(config=Config) -> Sanic:
    load_dotenv()
    app = Sanic("MyHelloWorldApp", config())
    app.register_listener(setup_db, "before_server_start")
    app.blueprint(helloworld_bp)
    return app
