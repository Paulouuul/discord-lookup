"""
Dependências para injeção do cliente Discord
"""

from fastapi import HTTPException
from discord_lookup import DiscordClient
from api.config import settings


def get_discord_client() -> DiscordClient:
    """Dependência para obter o cliente do Discord"""
    if not settings.is_token_configured:
        raise HTTPException(
            status_code=500,
            detail="DISCORD_BOT_TOKEN não configurado"
        )
    return DiscordClient(settings.DISCORD_BOT_TOKEN)