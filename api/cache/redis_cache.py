"""
Cache com Redis para a API
"""

import redis
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class RedisCache:
    """Cliente para cache Redis"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, ttl: int = 3600):
        """
        Inicializa o cliente Redis
        
        Args:
            host: Host do Redis
            port: Porta do Redis
            db: Banco de dados Redis
            ttl: Tempo de vida do cache em segundos (padrão: 1 hora)
        """
        self.ttl = ttl
        try:
            self.client = redis.Redis(
                host=host, 
                port=port, 
                db=db, 
                decode_responses=True,
                socket_connect_timeout=5
            )
            self.client.ping()  # Testa conexão
            logger.info(f"Conectado ao Redis em {host}:{port}")
        except redis.ConnectionError as e:
            logger.warning(f"Redis não disponível: {e}. Cache desabilitado.")
            self.client = None
    
    @property
    def is_available(self) -> bool:
        """Verifica se o Redis está disponível"""
        return self.client is not None
    
    def get(self, key: str) -> Optional[dict]:
        """Obtém um valor do cache"""
        if not self.is_available:
            return None
        try:
            data = self.client.get(key)
            if data:
                logger.info(f" CACHE HIT: {key}")
            else:
                logger.info(f" CACHE MISS: {key}")
            return json.loads(data) if data else None
        except Exception as e:
            logger.debug(f"Erro ao ler cache: {e}")
            return None
    
    def set(self, key: str, value: dict) -> None:
        """Armazena um valor no cache"""
        if not self.is_available:
            return
        try:
            self.client.setex(key, self.ttl, json.dumps(value))
        except Exception as e:
            logger.debug(f"Erro ao escrever cache: {e}")
    
    def delete(self, key: str) -> None:
        """Remove um valor do cache"""
        if not self.is_available:
            return
        try:
            self.client.delete(key)
        except Exception as e:
            logger.debug(f"Erro ao deletar cache: {e}")
    
    def clear(self, pattern: str = "user:*") -> None:
        """Limpa o cache por padrão"""
        if not self.is_available:
            return
        try:
            for key in self.client.scan_iter(pattern):
                self.client.delete(key)
        except Exception as e:
            logger.debug(f"Erro ao limpar cache: {e}")