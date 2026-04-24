"""
Configurações da aplicação
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configurações centralizadas"""
    
    # Discord
    DISCORD_BOT_TOKEN: str = os.getenv('DISCORD_BOT_TOKEN', '')
    
    # Redis
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    CACHE_TTL: int = int(os.getenv('CACHE_TTL', '3600'))
    
    # API
    API_TITLE: str = "Discord Lookup API"
    API_DESCRIPTION: str = "API para consulta de usuários do Discord"
    API_VERSION: str = "1.0.0"
    
    # Server
    HOST: str = os.getenv('API_HOST', '0.0.0.0')
    PORT: int = int(os.getenv('API_PORT', '8000'))
    RELOAD: bool = os.getenv('API_RELOAD', 'True').lower() == 'true'
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Rate Limiting (futuro)
    RATE_LIMIT_PER_MINUTE: int = 60
    
    @property
    def is_token_configured(self) -> bool:
        return bool(self.DISCORD_BOT_TOKEN)


settings = Settings()