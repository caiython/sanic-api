from pydantic import BaseModel, constr, Field
from typing import Annotated, Optional
from datetime import date, datetime
from uuid import uuid4

class GameSchema(BaseModel):
    uuid: str = Field(default_factory=lambda: uuid4().hex)
    title: Annotated[str, constr(max_length=100)]
    release_date: date
    creation_datetime: datetime = Field(default_factory=lambda: datetime.now())

    def to_dict(self) -> dict:
        game_json = self.model_dump()
        game_json['release_date'] = self.release_date.strftime('%Y-%m-%d')
        game_json['creation_datetime'] = self.creation_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
        return game_json

class GameUpdateSchema(BaseModel):
    title: Optional[Annotated[str, constr(max_length=100)]] = None
    release_date: Optional[date] = None
