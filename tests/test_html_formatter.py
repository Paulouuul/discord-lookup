"""
Testes para o HTMLFormatter
"""

import os
import tempfile
import pytest
from discord_lookup.formatters import HTMLFormatter
from discord_lookup.models import DiscordUser


class TestHTMLFormatter:
    """Testes para o HTMLFormatter"""
    
    def test_format_user_to_html(self):
        """Testa conversão de um usuário para HTML"""
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
        
        result = HTMLFormatter.format(user)
        
        assert "<!DOCTYPE html>" in result
        assert "<title>Discord User: testuser</title>" in result
        assert "123456789012345678" in result
        assert "testuser" in result
        assert "Test User" in result
        assert "</html>" in result
    
    def test_format_user_without_global_name(self):
        """Testa usuário sem global_name"""
        user = DiscordUser(
            id="123456789012345678",
            username="testuser2",
            discriminator="0000",
            avatar=None,
            bot=False,
            public_flags=0,
            global_name=None,
            banner=None
        )
        
        result = HTMLFormatter.format(user)
        
        assert "N/A" in result or "No banner" in result
    
    def test_save_html_to_file(self):
        """Testa salvar usuário em arquivo HTML"""
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
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            HTMLFormatter.save_to_file(user, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "testuser" in content
            assert "123456789012345678" in content
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_format_batch_to_html(self):
        """Testa conversão de batch para HTML"""
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
        
        result = HTMLFormatter.format_batch(results)
        
        assert "<!DOCTYPE html>" in result
        assert "Discord Batch Results" in result
        assert "Total" in result
        assert "SUCCESS" in result
        assert "ERROR" in result
    
    def test_save_batch_html_to_file(self):
        """Testa salvar batch em arquivo HTML"""
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
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            HTMLFormatter.save_batch_to_file(results, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "user1" in content
            assert "SUCCESS" in content
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)