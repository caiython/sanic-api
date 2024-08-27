from sanic import Sanic
from sanic.response import text
from dotenv import load_dotenv
from .config import Config
from .listeners import setup_db

def create_app(config=Config) -> Sanic:
    load_dotenv()
    app = Sanic("MyHelloWorldApp", config())
    app.register_listener(setup_db, "before_server_start")

    @app.get("/")
    async def hello_world(request):
        return text("Hello, world.")
    return app
