"""
Use case: Buscar um único usuário
"""

from fastapi import HTTPException
from discord_lookup import DiscordClient
from api.models.schemas import UserResponse
from api.cache import RedisCache


class GetUserUseCase:
    """Use case para buscar um usuário do Discord"""
    
    def __init__(self, client: DiscordClient, cache: RedisCache = None):
        self.client = client
        self.cache = cache
    
    def execute(self, user_id: str) -> UserResponse:
        """
        Executa a busca de um usuário
        
        Args:
            user_id: ID do usuário do Discord
            
        Returns:
            UserResponse: Dados do usuário formatados
            
        Raises:
            HTTPException: Se usuário não for encontrado ou erro na API
        """

        cache_key = f"user:{user_id}"
        if self.cache and self.cache.is_available:
            cached = self.cache.get(cache_key)
            if cached:
                return UserResponse(**cached)
        try:
            user = self.client.get_user(user_id)
            
            result = UserResponse(
                id=user.id,
                username=user.username,
                discriminator=user.discriminator,
                global_name=user.global_name,
                avatar_url=user.avatar_url,
                banner_url=user.banner_url,
                is_bot=user.is_bot,
                created_at=user.created_at,
                public_flags=user.public_flags
            )

            if self.cache and self.cache.is_available:
                self.cache.set(cache_key, result.model_dump())

            return result
        
            
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))