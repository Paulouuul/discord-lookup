"""
Testes para o CSVFormatter
"""

import os
import tempfile
import pytest
from discord_lookup.formatters import CSVFormatter
from discord_lookup.models import DiscordUser


class TestCSVFormatter:
    """Testes para o CSVFormatter"""
    
    def test_format_user_to_csv(self):
        """Testa conversão de um usuário para CSV"""
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
        
        result = CSVFormatter.format(user)
        
        assert "id,username,discriminator,global_name,avatar_url,banner_url,is_bot,created_at,public_flags" in result
        assert "123456789012345678" in result
        assert "testuser" in result
        assert "Test User" in result
    
    def test_save_csv_to_file(self):
        """Testa salvar usuário em arquivo CSV"""
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
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            CSVFormatter.save_to_file(user, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "testuser" in content
            assert "123456789012345678" in content
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_format_batch_to_csv(self):
        """Testa conversão de batch para CSV"""
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
                    "banner_url": None,
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
        
        result = CSVFormatter.format_batch(results)
        
        assert "user_id,success,username,discriminator,global_name,avatar_url,banner_url,created_at,is_bot,public_flags,error" in result
        assert "123456789012345678,SUCCESS,user1" in result
        assert "876543210987654321,ERROR" in result
        assert "Usuário não encontrado" in result
    
    def test_save_batch_csv_to_file(self):
        """Testa salvar batch em arquivo CSV"""
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
                    "banner_url": None,
                    "created_at": "01/01/2020 12:00",
                    "is_bot": False
                }
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            CSVFormatter.save_batch_to_file(results, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "user1" in content
            assert "SUCCESS" in content
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)