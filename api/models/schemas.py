"""
Modelos Pydantic para validação de dados
"""

from typing import Optional, List, Union
from pydantic import BaseModel


class UserResponse(BaseModel):
    """Resposta para um único usuário"""
    id: str
    username: str
    discriminator: str
    global_name: Optional[str] = None
    avatar_url: str
    banner_url: Optional[str] = None
    is_bot: bool
    created_at: str
    public_flags: int


class BatchUserData(BaseModel):
    """Dados de um usuário no batch"""
    id: str
    username: str
    discriminator: str
    global_name: Optional[str] = None
    avatar_url: str
    banner_url: Optional[str] = None
    created_at: str
    is_bot: bool
    public_flags: int = 0 


class BatchResultItem(BaseModel):
    """Item de resultado do batch"""
    user_id: str
    success: bool
    data: Optional[BatchUserData] = None
    error: Optional[str] = None


class BatchResponse(BaseModel):
    """Resposta para batch de usuários"""
    total: int
    success_count: int
    error_count: int
    results: List[BatchResultItem]


class BatchRequest(BaseModel):
    """Requisição para batch de usuários"""
    user_ids: List[str]


class ErrorResponse(BaseModel):
    """Resposta de erro"""
    detail: str