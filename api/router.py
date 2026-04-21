"""
Rotas para endpoints de usuários
Apenas definição de endpoints, sem lógica de negócio
"""

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from api.utils.csv_export import user_to_csv, batch_to_csv
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


@router.get(
    "/{user_id}",
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)
async def get_user(
    user_id: str,
    request: Request,
    client: DiscordClient = Depends(get_discord_client)
):
    """
    Busca informações de um usuário do Discord
    
    - **user_id**: ID numérico do usuário (17-20 dígitos)
    """
    use_case = GetUserUseCase(client)
    result = use_case.execute(user_id)
    accept = request.headers.get("accept", "application/json")
    
    if "text/csv" in accept:
        return Response(
            content=user_to_csv(result),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=user_{user_id}.csv"}
        )
    return JSONResponse(content=result.model_dump())


@router.post(
    "/batch",
    responses={500: {"model": ErrorResponse}}
)
async def get_users_batch(
    request: BatchRequest,
    req: Request,
    client: DiscordClient = Depends(get_discord_client)
):
    """
    Busca múltiplos usuários em lote
    
    - **user_ids**: Lista de IDs de usuários
    """
    use_case = GetUsersBatchUseCase(client)
    result = use_case.execute(request.user_ids)
    
    # Adicionar lógica do header
    accept = req.headers.get("accept", "application/json")
    
    if "text/csv" in accept:
        return Response(
            content=batch_to_csv(result),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=batch_results.csv"}
        )
    return JSONResponse(content=result.model_dump())