"""
Rotas para endpoints de usuários
Apenas definição de endpoints, sem lógica de negócio
"""

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from api.utils.exporters import Exporter
from typing import List
from discord_lookup import DiscordClient
from api.models.schemas import (
    UserResponse,
    BatchRequest,
    BatchResponse,
    ErrorResponse
)
from api.dependencies.discord_client import get_discord_client
from api.use_cases import GetUserUseCase, GetUsersBatchUseCase

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    request: Request,
    client: DiscordClient = Depends(get_discord_client)
):
    use_case = GetUserUseCase(client)
    result = use_case.execute(user_id)
    accept = request.headers.get("accept", "application/json")
    
    return Exporter.export(result, accept)


@router.post("/batch")
async def get_users_batch(
    request: BatchRequest,
    req: Request,
    client: DiscordClient = Depends(get_discord_client)
):
    use_case = GetUsersBatchUseCase(client)
    result = use_case.execute(request.user_ids)
    accept = req.headers.get("accept", "application/json")
    
    return Exporter.export_batch(result, accept)