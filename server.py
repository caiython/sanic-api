from sanic import Sanic
from sanic.response import text
import aiosqlite

app = Sanic("MyHelloWorldApp")

@app.before_server_start
async def attach_db(app, loop):
    app.ctx.db = await aiosqlite.connect("db.sqlite3")

@app.get("/")
async def hello_world(request):
    return text("Hello, world.")
