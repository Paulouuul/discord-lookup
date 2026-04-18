"""
Formatadores de saída para diferentes formatos (JSON, CSV, etc.)
"""

import json
from typing import Dict, Any


class JSONFormatter:
    """Formata a saída como JSON"""
    
    @staticmethod
    def format(user) -> str:
        """
        Converte o objeto DiscordUser para JSON formatado
        
        Args:
            user: Objeto DiscordUser
            
        Returns:
            str: JSON formatado com indentação
        """
        data = {
            "id": user.id,
            "username": user.username,
            "discriminator": user.discriminator,
            "global_name": user.global_name,
            "avatar_url": user.avatar_url,
            "banner_url": user.banner_url,
            "is_bot": user.is_bot,
            "created_at": user.created_at,
            "public_flags": user.public_flags
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def save_to_file(user, filename: str) -> None:
        """
        Salva o resultado em um arquivo JSON
        
        Args:
            user: Objeto DiscordUser
            filename: Nome do arquivo para salvar
        """
        data = {
            "id": user.id,
            "username": user.username,
            "discriminator": user.discriminator,
            "global_name": user.global_name,
            "avatar_url": user.avatar_url,
            "banner_url": user.banner_url,
            "is_bot": user.is_bot,
            "created_at": user.created_at,
            "public_flags": user.public_flags
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    @staticmethod
    def format_batch(results: list) -> str:
        """
        Formata resultados de batch como JSON
        
        Args:
            results: Lista de resultados do batch processing
            
        Returns:
            str: JSON formatado com estatísticas e resultados
        """
        output = {
            "total": len(results),
            "success_count": sum(1 for r in results if r['success']),
            "error_count": sum(1 for r in results if not r['success']),
            "results": results
        }
        return json.dumps(output, indent=2, ensure_ascii=False)
    
    @staticmethod
    def save_batch_to_file(results: list, filename: str) -> None:
        """
        Salva resultados de batch em arquivo JSON
        
        Args:
            results: Lista de resultados do batch processing
            filename: Nome do arquivo para salvar
        """
        output = {
            "total": len(results),
            "success_count": sum(1 for r in results if r['success']),
            "error_count": sum(1 for r in results if not r['success']),
            "results": results
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)