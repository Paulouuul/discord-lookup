"""
Rotas para endpoints de usuários
Apenas definição de endpoints, sem lógica de negócio
"""

from fastapi import APIRouter, Depends, Request
from api.cache import RedisCache
from api.utils.exporters import Exporter
from discord_lookup import DiscordClient
from api.models.schemas import BatchRequest
from api.dependencies.discord_client import get_discord_client
from api.dependencies.cache import get_cache
from api.use_cases import GetUserUseCase, GetUsersBatchUseCase

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    request: Request,
    client: DiscordClient = Depends(get_discord_client),
    cache: RedisCache = Depends(get_cache)
):
    use_case = GetUserUseCase(client, cache)
    result = use_case.execute(user_id)
    accept = request.headers.get("accept", "application/json")
    
    return Exporter.export(result, accept)


@router.post("/batch")
async def get_users_batch(
    request: BatchRequest,
    req: Request,
    client: DiscordClient = Depends(get_discord_client),
    cache: RedisCache = Depends(get_cache)
):
    use_case = GetUsersBatchUseCase(client, cache)
    result = use_case.execute(request.user_ids)
    accept = req.headers.get("accept", "application/json")
    
    return Exporter.export_batch(result, accept)