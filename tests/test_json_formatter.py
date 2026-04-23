"""
Testes para o JSONFormatter
"""

import json
import os
import tempfile
import pytest
from discord_lookup.formatters import JSONFormatter
from discord_lookup.models import DiscordUser


class TestJSONFormatter:
    """Testes para o JSONFormatter"""
    
    def test_format_user_to_json(self):
        """Testa conversão de um usuário para JSON"""
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
        
        result = JSONFormatter.format(user)
        data = json.loads(result)
        
        assert data["id"] == "123456789012345678"
        assert data["username"] == "testuser"
        assert data["discriminator"] == "1234"
        assert data["global_name"] == "Test User"
        assert data["is_bot"] is False
        assert "avatar_url" in data
        assert data["banner_url"] is None
    
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
        
        result = JSONFormatter.format(user)
        data = json.loads(result)
        
        assert data["global_name"] is None
        assert "avatar_url" in data
    
    def test_format_user_with_banner(self):
        """Testa usuário com banner"""
        user = DiscordUser(
            id="123456789012345678",
            username="testuser",
            discriminator="0000",
            avatar="abc123",
            bot=False,
            public_flags=0,
            global_name=None,
            banner="banner456"
        )
        
        result = JSONFormatter.format(user)
        data = json.loads(result)
        
        assert data["banner_url"] is not None
        assert "banner456" in data["banner_url"]
    
    def test_save_to_file(self):
        """Testa salvar usuário em arquivo JSON"""
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
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            JSONFormatter.save_to_file(user, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert data["id"] == "123456789012345678"
            assert data["username"] == "testuser"
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_format_batch(self):
        """Testa formatação de resultados de batch"""
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
        
        result = JSONFormatter.format_batch(results)
        data = json.loads(result)
        
        assert data["total"] == 2
        assert data["success_count"] == 1
        assert data["error_count"] == 1
        assert len(data["results"]) == 2
    
    def test_save_batch_to_file(self):
        """Testa salvar resultados de batch em arquivo JSON"""
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
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            JSONFormatter.save_batch_to_file(results, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert data["total"] == 1
            assert data["success_count"] == 1
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_format_batch_empty_results(self):
        """Testa formatação de batch vazio"""
        results = []
        
        result = JSONFormatter.format_batch(results)
        data = json.loads(result)
        
        assert data["total"] == 0
        assert data["success_count"] == 0
        assert data["error_count"] == 0
        assert len(data["results"]) == 0


class TestJSONFormatterEdgeCases:
    """Testes de casos extremos para o JSONFormatter"""
    
    def test_format_user_special_characters(self):
        """Testa usuário com caracteres especiais"""
        user = DiscordUser(
            id="123456789012345678",
            username="usuário_teste!@#$",
            discriminator="0000",
            avatar=None,
            bot=False,
            public_flags=0,
            global_name="Nome com ç e acentuação",
            banner=None
        )
        
        result = JSONFormatter.format(user)
        data = json.loads(result)
        
        assert data["username"] == "usuário_teste!@#$"
        assert data["global_name"] == "Nome com ç e acentuação"
    
    def test_format_user_very_long_fields(self):
        """Testa usuário com campos muito longos"""
        long_name = "a" * 1000
        user = DiscordUser(
            id="123456789012345678",
            username=long_name,
            discriminator="0000",
            avatar=None,
            bot=False,
            public_flags=0,
            global_name=long_name,
            banner=None
        )
        
        result = JSONFormatter.format(user)
        data = json.loads(result)
        
        assert len(data["username"]) == 1000
        assert len(data["global_name"]) == 1000
    
    def test_format_user_minimal_data(self):
        """Testa usuário com dados mínimos"""
        user = DiscordUser(
            id="123",
            username="minimal",
            discriminator="0000",
            avatar=None,
            bot=False,
            public_flags=0,
            global_name=None,
            banner=None
        )
        
        result = JSONFormatter.format(user)
        data = json.loads(result)
        
        assert data["id"] == "123"
        assert data["username"] == "minimal"
        assert data["banner_url"] is None
        assert "avatar_url" in data