"""
Utilitários para exportação de dados em CSV
"""

import csv
from io import StringIO
from api.models.schemas import UserResponse, BatchResponse


def user_to_csv(user: UserResponse) -> str:
    """
    Converte um único usuário para formato CSV
    
    Args:
        user: Dados do usuário
        
    Returns:
        str: Conteúdo CSV
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
    
    # Dados
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


def batch_to_csv(batch: BatchResponse) -> str:
    """
    Converte resultados de batch para formato CSV
    
    Args:
        batch: Resposta do batch
        
    Returns:
        str: Conteúdo CSV
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
        "created_at",
        "is_bot",
        "error"
    ])
    
    # Dados
    for result in batch.results:
        if result.success and result.data:
            writer.writerow([
                result.user_id,
                "SUCCESS",
                result.data.username,
                result.data.discriminator,
                result.data.global_name or "",
                result.data.avatar_url,
                result.data.created_at,
                result.data.is_bot,
                ""
            ])
        else:
            writer.writerow([
                result.user_id,
                "ERROR",
                "",
                "",
                "",
                "",
                "",
                "",
                result.error or "Unknown error"
            ])
    
    return output.getvalue()