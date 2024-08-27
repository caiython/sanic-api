import aiosqlite

async def setup_db(app):
    app.ctx.db = await aiosqlite.connect(app.config.DB_PATH)