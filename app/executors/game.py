from mayim import SQLiteExecutor, query
from app.schemas import GameSchema, GameUpdateSchema
from datetime import date, datetime
from uuid import UUID
from mayim.exception import RecordNotFound


class GameExecutor(SQLiteExecutor):
    
    async def select_all_games(self, limit_value: int = 10, offset_value: int = 0) -> list[GameSchema]:
        ...

    async def insert_game(self, uuid: UUID, title: str, release_date: date, creation_datetime: datetime) -> GameSchema:
        ...
    
    async def select_game(self, uuid: UUID) -> GameSchema:
        ...

    async def update_game(self, uuid: UUID, game_update_data: GameUpdateSchema) -> GameSchema:
        
        fields_to_update = []
        params = {"uuid": uuid}
        
        for field, value in game_update_data.model_dump(exclude_unset=True).items():
            fields_to_update.append(f"{field} = ${field}")
            params[field] = value

        if not fields_to_update:
            raise ValueError("No fields provided to update.")

        set_clause = ", ".join(fields_to_update)
        query = f"""
            UPDATE app_game
            SET {set_clause}
            WHERE uuid = $uuid
            RETURNING uuid, title, release_date, creation_datetime;
        """

        result = await self.execute(query, params=params)
        if not result:
            raise RecordNotFound(f"No game found with UUID {uuid}")

        return GameSchema(**result.__dict__)

    async def delete_game(self, uuid: UUID) -> GameSchema:
        ...