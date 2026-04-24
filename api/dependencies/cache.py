"""
Dependência para injeção do cache
"""
import logging
from api.cache import RedisCache
from api.config import settings

logger = logging.getLogger(__name__)


def get_cache() -> RedisCache:
    """
    Dependência para obter instância do cache Redis
    
    Returns:
        RedisCache: Instância configurada
    """
    logger.info("Criando instância do RedisCache...")
    cache = RedisCache(
        host=getattr(settings, 'REDIS_HOST', 'localhost'),
        port=getattr(settings, 'REDIS_PORT', 6379),
        ttl=getattr(settings, 'CACHE_TTL', 3600)
    )
    logger.info(f"Redis disponível: {cache.is_available}")  # ← ADICIONAR
    return cache