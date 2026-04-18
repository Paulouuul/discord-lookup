"""
Discord User Lookup Tool - Ferramenta CLI para consulta de usuários do Discord

Uma ferramenta profissional para buscar informações de usuários do Discord
usando a API oficial, com suporte a múltiplos formatos de saída, cache,
batch processing e containerização Docker.
"""

__version__ = "1.0.0"
__author__ = "Paulo Ricardo Tebet Lyrio"
__license__ = "MIT"

from discord_lookup.client import DiscordClient
from discord_lookup.models import DiscordUser
from discord_lookup.utils import snowflake_to_timestamp

__all__ = [
    "DiscordClient",
    "DiscordUser", 
    "snowflake_to_timestamp",
]