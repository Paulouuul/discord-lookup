#client.py
"""
Cliente para API do Discord
Gerencia requisições, autenticação e tratamento de erros
"""

import requests
import time
import logging
from tqdm import tqdm
from discord_lookup.models import DiscordUser

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
            if e.response is not None:
                if e.response.status_code == 404:
                    raise ValueError(f"Usuário {user_id} não encontrado")
                elif e.response.status_code == 401:
                    raise ValueError("Token inválido. Verifique seu DISCORD_BOT_TOKEN")
                else:
                    raise DiscordAPIError(f"Erro HTTP {e.response.status_code}: {e.response.text}")
            else:
                raise DiscordAPIError(f"Erro HTTP: {str(e)}")
        except requests.exceptions.Timeout:
            raise DiscordAPIError("Timeout na requisição - API do Discord demorou para responder")
        except requests.exceptions.ConnectionError:
            raise DiscordAPIError("Erro de conexão - verifique sua internet")
    def get_users_batch(self, user_ids: list, show_progress: bool = True) -> list:
        """
        Busca múltiplos usuários em lote
        
        Args:
            user_ids: Lista de IDs de usuários
            show_progress: Se deve mostrar barra de progresso
            
        Returns:
            list: Lista de dicionários com resultados (inclui erros)
        """
        results = []
        iterator = tqdm(user_ids, desc="Buscando usuários", disable=not show_progress) if show_progress else user_ids
        
        for user_id in iterator:
            try:
                user = self.get_user(user_id)
                results.append({
                    "user_id": user_id,
                    "success": True,
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "discriminator": user.discriminator,
                        "global_name": user.global_name,
                        "avatar_url": user.avatar_url,
                        "banner_url": user.banner_url,
                        "created_at": user.created_at,
                        "is_bot": user.is_bot,
                        "public_flags": user.public_flags
                    }
                })
            except Exception as e:
                results.append({
                    "user_id": user_id,
                    "success": False,
                    "error": str(e)
                })
        
        return results