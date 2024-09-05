from sanic.request import Request
from sanic.response import json
from sanic.exceptions import InvalidUsage, NotFound
from sanic import Blueprint

from app.executors import GameExecutor
from app.schemas import GameSchema, GameUpdateSchema

from pydantic import ValidationError
from mayim.exception import RecordNotFound
from uuid import UUID

game_bp = Blueprint('Game', url_prefix='/game')

@game_bp.get('/')
async def list_all_games(request: Request, executor: GameExecutor) -> json:

    limit = int(request.args.get('limit', 5))
    offset = int(request.args.get('offset', 0))

    if limit < 1:
        raise InvalidUsage('Limit must be a positive integer.')

    if offset < 0:
        raise InvalidUsage('Offset cannot be negative.')
    
    games = await executor.select_all_games(limit_value=limit, offset_value=offset)
    return json({'games': [game.to_dict() for game in games]})

@game_bp.post('/')
async def insert_game(request: Request, executor: GameExecutor) -> json:

    if not request.json or not isinstance(request.json, dict):
        return json({'error': 'Request body must be a valid JSON object.'}, status=400)
    
    try:
        game = GameSchema(**request.json)
    except ValidationError as e:
        return json({'errors': e.errors()}, status=400)

    await executor.insert_game(**game.model_dump())

    return json(game.to_dict(), status=201)

@game_bp.get('/<uuid>')
async def select_game(request: Request, executor: GameExecutor, uuid: str) -> json:
    try:
        UUID(uuid)
    except ValueError:
        raise InvalidUsage('UUID must be in a valid format.')
    
    try:
        game = await executor.select_game(uuid=uuid)
    except RecordNotFound:
        raise NotFound(f"Could not find game with uuid {uuid}")

    return json(game.to_dict())

@game_bp.patch('/<uuid>')
async def update_game(request: Request, executor: GameExecutor, uuid: str) -> json:

    if not request.json or not isinstance(request.json, dict):
        raise InvalidUsage('Request body must be a valid JSON object.')

    try:
        UUID(uuid)
    except ValueError:
        raise InvalidUsage('UUID must be in a valid format.')
    
    try:
        game_update_data = GameUpdateSchema(**request.json)
    except ValidationError as e:
        return json({'errors': e.errors()}, status=400)
    
    updated_game = await executor.update_game(uuid=uuid, game_update_data=game_update_data)

    return json(updated_game.to_dict())
