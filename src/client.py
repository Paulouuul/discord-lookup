"""
Cliente para API do Discord
Gerencia requisições, autenticação e tratamento de erros
"""

import requests
import time
import logging
from src.models import DiscordUser

logger = logging.getLogger(__name__)


class DiscordAPIError(Exception):
    """Exceção para erros da API do Discord"""
    pass


class DiscordClient:
    """
    Cliente para a API do Discord
    
    Attributes:
        token (str): Token do bot do Discord
        base_url (str): URL base da API (padrão: v10)
        timeout (int): Timeout para requisições em segundos
    """
    
    def __init__(self, token: str, timeout: int = 30):
        """
        Inicializa o cliente da API do Discord
        
        Args:
            token: Token do bot do Discord
            timeout: Timeout para requisições em segundos
        """
        self.token = token
        self.timeout = timeout
        self.base_url = "https://discord.com/api/v10"
        self.headers = {
            "Authorization": f"Bot {token}",
            "User-Agent": "DiscordUserLookup/1.0 (https://github.com/Paulouuul/discord-lookup)"
        }
    
    def get_user(self, user_id: str) -> DiscordUser:
        """
        Busca informações de um usuário pelo ID
        
        Args:
            user_id: ID numérico do usuário do Discord
            
        Returns:
            DiscordUser: Objeto com dados do usuário
            
        Raises:
            ValueError: Se o ID for inválido ou usuário não encontrado
            DiscordAPIError: Se houver erro na API (token inválido, rate limit, etc.)
        """
        # Validação básica do ID
        if not user_id.isdigit():
            raise ValueError(f"ID inválido: '{user_id}' - deve conter apenas números")
        
        if len(user_id) < 17 or len(user_id) > 20:
            raise ValueError(f"ID inválido: '{user_id}' - deve ter entre 17 e 20 dígitos")
        
        url = f"{self.base_url}/users/{user_id}"
        
        logger.info(f"Buscando usuário: {user_id}")
        
        try:
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=self.timeout
            )
            
            logger.debug(f"Status code: {response.status_code}")
            
            # Tratamento de rate limiting
            if response.status_code == 429:
                retry_after = response.json().get('retry_after', 1)
                logger.warning(f"Rate limit atingido. Aguardando {retry_after}s...")
                time.sleep(retry_after)
                return self.get_user(user_id)  # Tenta novamente
            
            response.raise_for_status()
            
            data = response.json()
            
            logger.debug(f"Usuário encontrado: {data.get('username')}")
            
            return DiscordUser(
                id=data.get('id'),
                username=data.get('username'),
                discriminator=data.get('discriminator', '0000'),
                avatar=data.get('avatar'),
                bot=data.get('bot', False),
                public_flags=data.get('public_flags', 0),
                global_name=data.get('global_name'),
                banner=data.get('banner')
            )
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(f"Usuário {user_id} não encontrado")
            elif response.status_code == 401:
                raise ValueError("Token inválido. Verifique seu DISCORD_BOT_TOKEN")
            else:
                raise DiscordAPIError(f"Erro HTTP {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            raise DiscordAPIError("Timeout na requisição - API do Discord demorou para responder")
        except requests.exceptions.ConnectionError:
            raise DiscordAPIError("Erro de conexão - verifique sua internet")