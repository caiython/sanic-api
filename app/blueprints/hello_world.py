from sanic.request import Request
from sanic.response import text
from sanic import Blueprint

helloworld_bp = Blueprint("HelloWorld", url_prefix='/hello_world')

@helloworld_bp.get("/")
async def root(request: Request) -> text:
    return text("Hello, world.")
