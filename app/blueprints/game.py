from sanic.request import Request
from sanic.response import json
from sanic.exceptions import InvalidUsage
from sanic import Blueprint

from app.executors import GameExecutor
from app.schemas import GameSchema

from pydantic import ValidationError

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