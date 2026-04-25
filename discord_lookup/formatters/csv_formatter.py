import csv
from io import StringIO
from discord_lookup.formatters.base import BaseFormatter


class CSVFormatter(BaseFormatter):
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
        
        # Dados do usuário (usando o método utilitário)
        data = BaseFormatter.get_user_data(user)
        writer.writerow([
            data["id"],
            data["username"],
            data["discriminator"],
            data["global_name"] or "",
            data["avatar_url"],
            data["banner_url"] or "",
            data["is_bot"],
            data["created_at"],
            data["public_flags"]
        ])
        
        return output.getvalue()
    
    @staticmethod
    def save_to_file(user, filename: str) -> None:
        """Salva um único usuário em arquivo CSV"""
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
            "is_bot",
            "created_at",
            "public_flags",
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
                    data.get('is_bot', False),
                    data.get('created_at', ''),
                    data.get('public_flags', 0),
                    ""
                ])
            else:
                writer.writerow([
                    result['user_id'],
                    "ERROR",
                    "", "", "", "", "", "", "",
                    result.get('error', 'Erro desconhecido')
                ])
        
        return output.getvalue()
    
    @staticmethod
    def save_batch_to_file(results: list, filename: str) -> None:
        """Salva resultados de batch em arquivo CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            f.write(CSVFormatter.format_batch(results))