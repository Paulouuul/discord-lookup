#formatters.py
"""
Formatadores de saída para diferentes formatos (JSON, CSV)
"""
import csv
import yaml
from io import StringIO
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

class CSVFormatter:
    """Formata a saída como CSV"""
    
    @staticmethod
    def format(user) -> str:
        """
        Converte um único usuário para CSV
        
        Args:
            user: Objeto DiscordUser
            
        Returns:
            str: CSV com cabeçalho e uma linha de dados
        """
        output = StringIO()
        writer = csv.writer(output)
        
        # Cabeçalho
        writer.writerow([
            "id", 
            "username", 
            "discriminator", 
            "global_name", 
            "avatar_url", 
            "banner_url",
            "is_bot", 
            "created_at", 
            "public_flags"
        ])
        
        # Dados do usuário
        writer.writerow([
            user.id,
            user.username,
            user.discriminator,
            user.global_name or "",
            user.avatar_url,
            user.banner_url or "",
            user.is_bot,
            user.created_at,
            user.public_flags
        ])
        
        return output.getvalue()
    
    @staticmethod
    def save_to_file(user, filename: str) -> None:
        """
        Salva um único usuário em arquivo CSV
        
        Args:
            user: Objeto DiscordUser
            filename: Nome do arquivo para salvar
        """
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            f.write(CSVFormatter.format(user))
    
    @staticmethod
    def format_batch(results: list) -> str:
        """
        Converte resultados de batch para CSV
        
        Args:
            results: Lista de resultados do batch processing
            
        Returns:
            str: CSV com todos os resultados (sucessos e erros)
        """
        output = StringIO()
        writer = csv.writer(output)
        
        # Cabeçalho
        writer.writerow([
            "user_id",
            "success",
            "username",
            "discriminator",
            "global_name",
            "avatar_url",
            "banner_url",
            "created_at",
            "is_bot",
            "error"
        ])
        
        # Dados
        for result in results:
            if result['success']:
                data = result['data']
                writer.writerow([
                    result['user_id'],
                    "SUCCESS",
                    data.get('username', ''),
                    data.get('discriminator', ''),
                    data.get('global_name') or '',
                    data.get('avatar_url', ''),
                    data.get('banner_url') or '',
                    data.get('created_at', ''),
                    data.get('is_bot', False),
                    ""  # sem erro
                ])
            else:
                writer.writerow([
                    result['user_id'],
                    "ERROR",
                    "",  # username
                    "",  # discriminator
                    "",  # global_name
                    "",  # avatar_url
                    "",  # banner_url
                    "",  # created_at
                    "",  # is_bot
                    result.get('error', 'Erro desconhecido')
                ])
        
        return output.getvalue()
    
    @staticmethod
    def save_batch_to_file(results: list, filename: str) -> None:
        """
        Salva resultados de batch em arquivo CSV
        
        Args:
            results: Lista de resultados do batch processing
            filename: Nome do arquivo para salvar
        """
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            f.write(CSVFormatter.format_batch(results))