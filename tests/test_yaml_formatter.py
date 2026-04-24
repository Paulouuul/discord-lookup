"""
Testes para o YAMLFormatter
"""

import os
import tempfile
import pytest
import yaml
from discord_lookup.formatters import YAMLFormatter
from discord_lookup.models import DiscordUser


class TestYAMLFormatter:
    """Testes para o YAMLFormatter"""
    
    def test_format_user_to_yaml(self):
        """Testa conversão de um usuário para YAML"""
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
        
        result = YAMLFormatter.format(user)
        data = yaml.safe_load(result)
        
        assert data["id"] == "123456789012345678"
        assert data["username"] == "testuser"
        assert data["discriminator"] == "1234"
        assert data["global_name"] == "Test User"
        assert data["is_bot"] is False
        assert "avatar_url" in data
        assert "banner_url" in data
        assert "created_at" in data
        assert "public_flags" in data
        assert data["public_flags"] == 0
    
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
        
        result = YAMLFormatter.format(user)
        data = yaml.safe_load(result)
        
        assert data["global_name"] is None
    
    def test_save_yaml_to_file(self):
        """Testa salvar usuário em arquivo YAML"""
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
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            YAMLFormatter.save_to_file(user, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            assert data["id"] == "123456789012345678"
            assert data["username"] == "testuser"
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_format_batch_to_yaml(self):
        """Testa conversão de batch para YAML"""
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
                    "banner_url": "https://example.com/banner.png",
                    "created_at": "01/01/2020 12:00",
                    "is_bot": False,
                    "public_flags": 128
                }
            },
            {
                "user_id": "876543210987654321",
                "success": False,
                "error": "Usuário não encontrado"
            }
        ]
        
        result = YAMLFormatter.format_batch(results)
        data = yaml.safe_load(result)
        
        assert data["total"] == 2
        assert data["success_count"] == 1
        assert data["error_count"] == 1
        assert len(data["results"]) == 2
    
    def test_save_batch_yaml_to_file(self):
        """Testa salvar batch em arquivo YAML"""
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
                    "banner_url": "https://example.com/banner.png",
                    "created_at": "01/01/2020 12:00",
                    "is_bot": False,
                    "public_flags": 0
                }
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            YAMLFormatter.save_batch_to_file(results, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            assert data["total"] == 1
            assert data["success_count"] == 1
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_format_batch_empty_results(self):
        """Testa formatação de batch vazio"""
        results = []
        
        result = YAMLFormatter.format_batch(results)
        data = yaml.safe_load(result)
        
        assert data["total"] == 0
        assert data["success_count"] == 0
        assert data["error_count"] == 0
        assert len(data["results"]) == 0