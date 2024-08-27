from sanic import Sanic
from sanic.response import text
import aiosqlite
from config import Config

app = Sanic("MyHelloWorldApp", Config())

@app.before_server_start
async def attach_db(app, loop):
    app.ctx.db = await aiosqlite.connect(app.config.DB_PATH)

@app.get("/")
async def hello_world(request):
    return text("Hello, world.")
