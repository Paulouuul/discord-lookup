"""
Use case: Buscar um único usuário
"""

from fastapi import HTTPException
from discord_lookup import DiscordClient
from api.models.schemas import UserResponse


class GetUserUseCase:
    """Use case para buscar um usuário do Discord"""
    
    def __init__(self, client: DiscordClient):
        self.client = client
    
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
        try:
            user = self.client.get_user(user_id)
            
            return UserResponse(
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
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))