#utils.py
from datetime import datetime

def snowflake_to_timestamp(snowflake: str) -> str:
    """
    Converte Discord Snowflake ID em data de criação
    
    Args:
        snowflake: ID numérico do Discord
        
    Returns:
        str: Data formatada como DD/MM/AAAA HH:MM
    """
    timestamp = (int(snowflake) >> 22) + 1420070400000
    return datetime.fromtimestamp(timestamp / 1000).strftime("%d/%m/%Y %H:%M")