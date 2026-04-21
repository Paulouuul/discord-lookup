"""
Formatador YAML para saída de dados
"""

import yaml
from discord_lookup.formatters.base import BaseFormatter


class YAMLFormatter(BaseFormatter):
    """Formata a saída como YAML"""
    
    @staticmethod
    def format(user) -> str:
        """
        Converte um único usuário para YAML
        
        Args:
            user: Objeto DiscordUser
            
        Returns:
            str: YAML formatado
        """
        data = BaseFormatter.get_user_data(user)
        return yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False)
    
    @staticmethod
    def save_to_file(user, filename: str) -> None:
        """
        Salva um único usuário em arquivo YAML
        
        Args:
            user: Objeto DiscordUser
            filename: Nome do arquivo para salvar
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(YAMLFormatter.format(user))
    
    @staticmethod
    def format_batch(results: list) -> str:
        """
        Formata resultados de batch como YAML
        
        Args:
            results: Lista de resultados do batch processing
            
        Returns:
            str: YAML formatado com estatísticas e resultados
        """
        output = {
            "total": len(results),
            "success_count": sum(1 for r in results if r['success']),
            "error_count": sum(1 for r in results if not r['success']),
            "results": results
        }
        return yaml.dump(output, allow_unicode=True, sort_keys=False, default_flow_style=False)
    
    @staticmethod
    def save_batch_to_file(results: list, filename: str) -> None:
        """
        Salva resultados de batch em arquivo YAML
        
        Args:
            results: Lista de resultados do batch processing
            filename: Nome do arquivo para salvar
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(YAMLFormatter.format_batch(results))