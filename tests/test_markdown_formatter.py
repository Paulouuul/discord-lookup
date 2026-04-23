"""
Testes para o MarkdownFormatter
"""

import os
import tempfile
import pytest
from discord_lookup.formatters import MarkdownFormatter
from discord_lookup.models import DiscordUser


class TestMarkdownFormatter:
    """Testes para o MarkdownFormatter"""
    
    def test_format_user_to_markdown(self):
        """Testa conversão de um usuário para Markdown"""
        user = DiscordUser(
            id="123456789012345678",
            username="testuser",
            discriminator="1234",
            avatar="abc123",
            bot=False,
            public_flags=0,
            global_name="Test User",
            banner=None
        )
        
        result = MarkdownFormatter.format(user)
        
        assert "# Discord User: testuser" in result
        assert "| **ID** | `123456789012345678` |" in result
        assert "| **Username** | `testuser` |" in result
        assert "| **Bot** | Não |" in result
        assert "[Avatar URL]" in result
    
    def test_format_user_bot_true(self):
        """Testa usuário que é bot"""
        user = DiscordUser(
            id="123456789012345678",
            username="testbot",
            discriminator="0000",
            avatar=None,
            bot=True,
            public_flags=0,
            global_name=None,
            banner=None
        )
        
        result = MarkdownFormatter.format(user)
        
        assert "| **Bot** | Sim |" in result
    
    def test_save_markdown_to_file(self):
        """Testa salvar usuário em arquivo Markdown"""
        user = DiscordUser(
            id="123456789012345678",
            username="testuser",
            discriminator="0000",
            avatar=None,
            bot=False,
            public_flags=0,
            global_name=None,
            banner=None
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            MarkdownFormatter.save_to_file(user, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "testuser" in content
            assert "123456789012345678" in content
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_format_batch_to_markdown(self):
        """Testa conversão de batch para Markdown"""
        results = [
            {
                "user_id": "123456789012345678",
                "success": True,
                "data": {
                    "id": "123456789012345678",
                    "username": "user1",
                    "discriminator": "0000",
                    "global_name": None,
                    "avatar_url": "https://example.com/avatar1.png",
                    "created_at": "01/01/2020 12:00",
                    "is_bot": False
                }
            },
            {
                "user_id": "876543210987654321",
                "success": False,
                "error": "Usuário não encontrado"
            }
        ]
        
        result = MarkdownFormatter.format_batch(results)
        
        assert "# Discord Batch Results" in result
        assert "| **Total** | 2 |" in result
        assert "| **Sucessos** | 1 |" in result
        assert "| **Erros** | 1 |" in result
        assert "| 123456789012345678 | SUCCESS | user1" in result
        assert "| 876543210987654321 | ERROR" in result
    
    def test_save_batch_markdown_to_file(self):
        """Testa salvar batch em arquivo Markdown"""
        results = [
            {
                "user_id": "123456789012345678",
                "success": True,
                "data": {
                    "id": "123456789012345678",
                    "username": "user1",
                    "discriminator": "0000",
                    "global_name": None,
                    "avatar_url": "https://example.com/avatar1.png",
                    "created_at": "01/01/2020 12:00",
                    "is_bot": False
                }
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            MarkdownFormatter.save_batch_to_file(results, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "user1" in content
            assert "SUCCESS" in content
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_format_batch_empty_results(self):
        """Testa formatação de batch vazio"""
        results = []
        
        result = MarkdownFormatter.format_batch(results)
        
        assert "# Discord Batch Results" in result
        assert "| **Total** | 0 |" in result