"""
Use case: Buscar múltiplos usuários em lote
"""

from fastapi import HTTPException
from typing import List
from discord_lookup import DiscordClient
from api.models.schemas import BatchResponse, BatchResultItem
from api.cache import RedisCache


class GetUsersBatchUseCase:
    """Use case para buscar múltiplos usuários"""
    
    def __init__(self, client: DiscordClient, cache: RedisCache = None):
        self.client = client
        self.cache = cache
    
    def execute(self, user_ids: List[str]) -> BatchResponse:
        """
        Executa a busca em lote de usuários
        
        Args:
            user_ids: Lista de IDs de usuários
            
        Returns:
            BatchResponse: Resultados formatados com estatísticas
        """
        try:
            # results = self.client.get_users_batch(user_ids)

            results = []
            uncached_ids = []
            
             # ========== 1. VERIFICAR CACHE POR USUÁRIO ==========
            if self.cache and self.cache.is_available:
                for user_id in user_ids:
                    cache_key = f"user:{user_id}"
                    cached = self.cache.get(cache_key)
                    if cached:
                        # Usuário encontrado no cache
                        results.append({
                            "user_id": user_id,
                            "success": True,
                            "data": cached
                        })
                    else:
                        uncached_ids.append(user_id)
            else:
                uncached_ids = user_ids
            # ===================================================
            
            # ========== 2. BUSCAR USUÁRIOS NÃO CACHEADOS ==========
            if uncached_ids:
                # Buscar usando o método batch existente
                batch_results = self.client.get_users_batch(uncached_ids)
                
                for r in batch_results:
                    results.append(r)
                    
                    # Salvar no cache
                    if self.cache and self.cache.is_available and r['success']:
                        cache_key = f"user:{r['user_id']}"
                        self.cache.set(cache_key, r['data'])
            # ===================================================
            # Converter resultados para o formato esperado
            formatted_results = []
            for r in results:
                if r['success']:
                    data = r['data']
                    formatted_results.append(BatchResultItem(
                        user_id=r['user_id'],
                        success=True,
                        data={
                            "id": data['id'],
                            "username": data['username'],
                            "discriminator": data['discriminator'],
                            "global_name": data.get('global_name'),
                            "avatar_url": data['avatar_url'],
                            "banner_url": data.get('banner_url'),
                            "created_at": data['created_at'],
                            "is_bot": data['is_bot'],
                            "public_flags": data.get('public_flags', 0)
                        },
                        error=None
                    ))
                else:
                    formatted_results.append(BatchResultItem(
                        user_id=r['user_id'],
                        success=False,
                        data=None,
                        error=r.get('error', 'Erro desconhecido')
                    ))
            
            return BatchResponse(
                total=len(results),
                success_count=sum(1 for r in results if r['success']),
                error_count=sum(1 for r in results if not r['success']),
                results=formatted_results
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))