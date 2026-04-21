from abc import ABC, abstractmethod

class BaseFormatter(ABC):
    """Classe base abstrata para todos os formatadores"""
    
    @staticmethod
    @abstractmethod
    def format(user) -> str:
        """Converte um único usuário para o formato"""
        pass
    
    @staticmethod
    @abstractmethod
    def save_to_file(user, filename: str) -> None:
        """Salva um único usuário em arquivo"""
        pass
    
    @staticmethod
    @abstractmethod
    def format_batch(results: list) -> str:
        """Converte resultados de batch para o formato"""
        pass
    
    @staticmethod
    @abstractmethod
    def save_batch_to_file(results: list, filename: str) -> None:
        """Salva resultados de batch em arquivo"""
        pass

    @staticmethod
    def get_user_data(user) -> dict:
        """Retorna dados comuns do usuário"""
        return {
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
