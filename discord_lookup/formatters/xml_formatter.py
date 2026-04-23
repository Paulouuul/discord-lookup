"""
Formatador XML para saída de dados
"""

import xml.dom.minidom as minidom
from dicttoxml import dicttoxml
from discord_lookup.formatters.base import BaseFormatter


class XMLFormatter(BaseFormatter):
    """Formata a saída como XML"""
    
    @staticmethod
    def format(user) -> str:
        """
        Converte um único usuário para XML
        
        Args:
            user: Objeto DiscordUser
            
        Returns:
            str: XML formatado
        """
        data = BaseFormatter.get_user_data(user)
        
        # Converte dicionário para XML
        xml_bytes = dicttoxml(data, custom_root='user', attr_type=False)
        xml_str = xml_bytes.decode('utf-8')
        
        # Formata XML com indentação
        dom = minidom.parseString(xml_str)
        return dom.toprettyxml(indent="  ")
    
    @staticmethod
    def save_to_file(user, filename: str) -> None:
        """
        Salva um único usuário em arquivo XML
        
        Args:
            user: Objeto DiscordUser
            filename: Nome do arquivo para salvar
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(XMLFormatter.format(user))
    
    @staticmethod
    def format_batch(results: list) -> str:
        """
        Formata resultados de batch como XML
        
        Args:
            results: Lista de resultados do batch processing
            
        Returns:
            str: XML formatado com estatísticas e resultados
        """
        output = {
            "total": len(results),
            "success_count": sum(1 for r in results if r['success']),
            "error_count": sum(1 for r in results if not r['success']),
            "results": []
        }
        
        for result in results:
            if result['success']:
                output["results"].append({
                    "user_id": result['user_id'],
                    "success": "true",
                    "data": result['data']
                })
            else:
                output["results"].append({
                    "user_id": result['user_id'],
                    "success": "false",
                    "error": result.get('error', 'Unknown error')
                })
        
        xml_bytes = dicttoxml(output, custom_root='batch', attr_type=False)
        xml_str = xml_bytes.decode('utf-8')
        
        dom = minidom.parseString(xml_str)
        return dom.toprettyxml(indent="  ")
    
    @staticmethod
    def save_batch_to_file(results: list, filename: str) -> None:
        """
        Salva resultados de batch em arquivo XML
        
        Args:
            results: Lista de resultados do batch processing
            filename: Nome do arquivo para salvar
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(XMLFormatter.format_batch(results))