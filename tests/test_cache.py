import pytest
from api.cache import RedisCache


class TestCache:
    """Testes para o cache Redis"""
    
    def test_cache_set_and_get(self):
        """Testa armazenar e recuperar do cache"""
        cache = RedisCache()
        cache.set("test_key", {"value": "test"})
        result = cache.get("test_key")
        assert result["value"] == "test"
    
    def test_cache_miss(self):
        """Testa cache miss para chave inexistente"""
        cache = RedisCache()
        result = cache.get("nonexistent_key")
        assert result is None