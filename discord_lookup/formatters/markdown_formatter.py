"""
Formatador Markdown para saída de dados
"""

from discord_lookup.formatters.base import BaseFormatter


class MarkdownFormatter(BaseFormatter):
    """Formata a saída como Markdown"""
    
    @staticmethod
    def format(user) -> str:
        """
        Converte um único usuário para Markdown
        
        Args:
            user: Objeto DiscordUser
            
        Returns:
            str: Markdown formatado
        """
        data = BaseFormatter.get_user_data(user)
        
        return f"""# Discord User: {data['username']}

## Informações Básicas

| Campo | Valor |
|-------|-------|
| **ID** | `{data['id']}` |
| **Username** | `{data['username']}` |
| **Discriminator** | `#{data['discriminator']}` |
| **Global Name** | {data['global_name'] or 'N/A'} |
| **Bot** | {'Sim' if data['is_bot'] else 'Não'} |
| **Created At** | {data['created_at']} |
| **Public Flags** | {data['public_flags']} |

## Links

- [Avatar URL]({data['avatar_url']})
{f"- [Banner URL]({data['banner_url']})" if data['banner_url'] else ""}
---
*Gerado por Discord Lookup Tool*
"""
    
    @staticmethod
    def save_to_file(user, filename: str) -> None:
        """
        Salva um único usuário em arquivo Markdown
        
        Args:
            user: Objeto DiscordUser
            filename: Nome do arquivo para salvar
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(MarkdownFormatter.format(user))
    
    @staticmethod
    def format_batch(results: list) -> str:
        """
        Formata resultados de batch como Markdown
        
        Args:
            results: Lista de resultados do batch processing
            
        Returns:
            str: Markdown formatado com estatísticas e resultados
        """
        success_count = sum(1 for r in results if r['success'])
        error_count = len(results) - success_count
        
        rows = ""
        for result in results:
            if result['success']:
                data = result['data']
                rows += f"| {result['user_id']} | SUCCESS | {data['username'] or '-'} | {data['discriminator'] or '-'} | {data['global_name'] or '-'} | {data['avatar_url'] or '-'} | {data.get('banner_url') or '-'} | {data['created_at'] or '-'} | {data['is_bot'] or '-'} | {data.get('public_flags', 0) or '-'} | - |\n"
            else:
                rows += f"| {result['user_id']} | ERROR | - | - | - | - | - | - | - | - | {result.get('error', 'Unknown')} |\n"
        
        return f"""# Discord Batch Results

## Estatísticas

| Métrica | Valor |
|---------|-------|
| **Total** | {len(results)} |
| **Sucessos** | {success_count} |
| **Erros** | {error_count} |

## Resultados

| User ID | Status | Username | Discriminator | Global Name | Avatar URL | Banner URL | Created At | Is Bot | Public Flags | Error |
|---------|--------|----------|---------------|-------------|------------|------------|------------|-------|---------------|-------|
{rows}
---
*Gerado por Discord Lookup Tool*
"""
    
    @staticmethod
    def save_batch_to_file(results: list, filename: str) -> None:
        """
        Salva resultados de batch em arquivo Markdown
        
        Args:
            results: Lista de resultados do batch processing
            filename: Nome do arquivo para salvar
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(MarkdownFormatter.format_batch(results))