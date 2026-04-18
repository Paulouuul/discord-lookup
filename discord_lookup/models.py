from dataclasses import dataclass
from typing import Optional
from discord_lookup.utils import snowflake_to_timestamp

@dataclass
class DiscordUser:
    """Modelo de dados do usuário do Discord"""
    id: str
    username: str
    discriminator: str
    avatar: Optional[str]
    bot: Optional[bool] = False
    public_flags: Optional[int] = 0
    global_name: Optional[str] = None
    banner: Optional[str] = None
    
    @property
    def avatar_url(self) -> str:
        """Retorna URL completa do avatar"""
        if self.avatar:
            return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png?size=512"
        return "https://cdn.discordapp.com/embed/avatars/0.png"
    
    @property
    def banner_url(self) -> Optional[str]:
        """Retorna URL completa do banner"""
        if self.banner:
            return f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.png?size=512"
        return None
    
    @property
    def created_at(self) -> str:
        """Retorna data de criação da conta"""
        return snowflake_to_timestamp(self.id)
    
    @property
    def is_bot(self) -> bool:
        """Retorna se é um bot"""
        return self.bot or False