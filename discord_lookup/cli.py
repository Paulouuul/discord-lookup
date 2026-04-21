#cli.py
"""
Interface de Linha de Comando para o Discord User Lookup
"""

import sys
import argparse
from dotenv import load_dotenv
import os
import logging
from colorama import init, Fore, Style
from discord_lookup.formatters import JSONFormatter, CSVFormatter
from discord_lookup.client import DiscordClient

# Inicializa colorama para cores no terminal
init(autoreset=True)

# Configura logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def format_user_output(user, show_colors=True):
    """
    Formata a saída do usuário para exibição no terminal
    
    Args:
        user: Objeto DiscordUser
        show_colors: Se deve usar cores no output
    """
    if show_colors:
        logger.info(f"{Fore.GREEN}✅ USUÁRIO ENCONTRADO!{Style.RESET_ALL}")
        logger.info(f"{Fore.CYAN}ID:{Style.RESET_ALL} {user.id}")
        logger.info(f"{Fore.CYAN}Username:{Style.RESET_ALL} {user.username}")
        logger.info(f"{Fore.CYAN}Discriminator:{Style.RESET_ALL} #{user.discriminator}")
        logger.info(f"{Fore.CYAN}Nome Completo:{Style.RESET_ALL} {user.username}#{user.discriminator}")
        logger.info(f"{Fore.CYAN}Avatar:{Style.RESET_ALL} {user.avatar_url}")
        logger.info(f"{Fore.CYAN}Bot:{Style.RESET_ALL} {'Sim' if user.is_bot else 'Não'}")
        logger.info(f"{Fore.CYAN}Data Criação:{Style.RESET_ALL} {user.created_at}")
        logger.info(f"{Fore.CYAN}Badges/Flags:{Style.RESET_ALL} {user.public_flags}")
        logger.info(f"{Fore.CYAN}Global Name:{Style.RESET_ALL} {user.global_name or 'N/A'}")
        
        if user.banner:
            logger.info(f"{Fore.CYAN}Banner:{Style.RESET_ALL} {user.banner_url}")
    else:
        logger.info(f"✅ USUÁRIO ENCONTRADO!")
        logger.info(f"ID: {user.id}")
        logger.info(f"Username: {user.username}")
        logger.info(f"Discriminator: #{user.discriminator}")
        logger.info(f"Nome Completo: {user.username}#{user.discriminator}")
        logger.info(f"Avatar: {user.avatar_url}")
        logger.info(f"Bot: {'Sim' if user.is_bot else 'Não'}")
        logger.info(f"Data Criação: {user.created_at}")
        logger.info(f"Badges/Flags: {user.public_flags}")
        logger.info(f"Global Name: {user.global_name or 'N/A'}")
        
        if user.banner:
            logger.info(f"Banner: {user.banner_url}")


def main():
    """Função principal do CLI"""
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Obtém token
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("❌ Token não encontrado! Configure o arquivo .env com DISCORD_BOT_TOKEN")
        sys.exit(1)
    
    # Configura parser de argumentos
    parser = argparse.ArgumentParser(
        description="Discord User Lookup Tool - Busca informações de usuários do Discord",
        epilog="Exemplo: python -m discord_lookup.cli 123456789012345678"
    )
    
    parser.add_argument(
        'user_id',
        nargs='?',
        help='ID do usuário do Discord (17-20 dígitos)'
    )
    
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true',
        help='Modo verbose - mostra logs detalhados'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Desativa cores no output'
    )
    
    parser.add_argument(
        '--output',
        choices=['table', 'json', 'csv'],
        default='table',
        help='Formato de saída (table, json ou csv)'
    )
    
    parser.add_argument(
        '--save',
        metavar='ARQUIVO',
        help='Salvar resultado em arquivo (só funciona com --output json)'
    )
    
    parser.add_argument(
        '--batch',
        metavar='ARQUIVO',
        help='Arquivo com lista de IDs (um por linha) para processar em lote'
    )

    parser.add_argument(
        '--no-progress',
        action='store_true',
        help='Desativa barra de progresso no batch mode'
    )
    args = parser.parse_args()
    
    # Configura nível de log
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Modo verbose ativado")
    
    try:
        client = DiscordClient(token)
        
        # MODO BATCH
        if args.batch:
            # Ler IDs do arquivo
            # Ler IDs do arquivo com múltiplos encodings
            encodings = ['utf-8-sig', 'utf-8', 'utf-16', 'latin-1', 'cp1252']
            user_ids = None
            
            for encoding in encodings:
                try:
                    with open(args.batch, 'r', encoding=encoding) as f:
                        user_ids = [line.strip() for line in f if line.strip()]
                        if user_ids:
                            logger.debug(f"Arquivo lido com encoding: {encoding}")
                            break
                except (UnicodeDecodeError, UnicodeError):
                    continue
            if not user_ids:
                logger.error("❌ Arquivo vazio ou sem IDs válidos")
                sys.exit(1)
            
            logger.info(f"📋 Processando {len(user_ids)} usuários...")
            
            # Buscar em lote
            results = client.get_users_batch(user_ids, show_progress=not args.no_progress)
            
            # Estatísticas
            success_count = sum(1 for r in results if r['success'])
            error_count = len(results) - success_count
            
            logger.info(f"✅ Sucessos: {success_count} | ❌ Erros: {error_count}")
            
            # Salvar resultados se solicitado
            if args.save:
                if args.output == 'json':
                    JSONFormatter.save_batch_to_file(results, args.save)
                    logger.info(f"✅ Resultados salvos em: {args.save}")
                elif args.output == 'csv':
                    CSVFormatter.save_batch_to_file(results, args.save)
                    logger.info(f"✅ Resultados salvos em: {args.save}")
                else:
                    logger.warning("--save só funciona com --output json ou --output csv")
            
            # Exibir resultados
            if args.output == 'json':
                print(JSONFormatter.format_batch(results))
            elif args.output == 'csv':
                print(CSVFormatter.format_batch(results))
            else:
                for result in results:
                    if result['success']:
                        print(f"\n✅ {result['user_id']}: {result['data']['username']}")
                    else:
                        print(f"\n❌ {result['user_id']}: {result['error']}")
        
        # MODO SINGLE USER
        else:
            user = client.get_user(args.user_id)
            
            if args.save:
                if args.output == 'json':
                    JSONFormatter.save_to_file(user, args.save)
                    logger.info(f"✅ Resultado salvo em: {args.save}")
                elif args.output == 'csv':
                    CSVFormatter.save_to_file(user, args.save)
                    logger.info(f"✅ Resultado salvo em: {args.save}")
                else:
                    logger.warning("--save só funciona com --output json ou --output csv")
            
            if args.output == 'json':
                print(JSONFormatter.format(user))
            elif args.output == 'csv':
                print(CSVFormatter.format(user))
            else:
                format_user_output(user, show_colors=not args.no_color)
            
    except ValueError as e:
        logger.error(f"❌ Erro: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()