from mayim import SQLiteExecutor, query
from app.schemas import GameSchema
from datetime import date, datetime
from uuid import UUID


class GameExecutor(SQLiteExecutor):
    
    async def select_all_games(self, limit_value: int = 10, offset_value: int = 0) -> list[GameSchema]:
        ...

    async def insert_game(self, uuid: UUID, title: str, release_date: date, creation_datetime: datetime) -> GameSchema:
        ...
