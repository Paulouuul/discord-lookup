"""
Testes para o XMLFormatter
"""

import os
import tempfile
import pytest
import xml.etree.ElementTree as ET
from discord_lookup.formatters import XMLFormatter
from discord_lookup.models import DiscordUser


class TestXMLFormatter:
    """Testes para o XMLFormatter"""
    
    def test_format_user_to_xml(self):
        """Testa conversão de um usuário para XML"""
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
        
        result = XMLFormatter.format(user)
        
        assert "<user>" in result
        assert "<id>123456789012345678</id>" in result
        assert "<username>testuser</username>" in result
        assert "<discriminator>1234</discriminator>" in result
        assert "</user>" in result
    
    def test_save_xml_to_file(self):
        """Testa salvar usuário em arquivo XML"""
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
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            XMLFormatter.save_to_file(user, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "testuser" in content
            assert "123456789012345678" in content
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_format_batch_to_xml(self):
        """Testa conversão de batch para XML"""
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
        
        result = XMLFormatter.format_batch(results)
        
        assert "<batch>" in result
        assert "<total>2</total>" in result
        assert "<success_count>1</success_count>" in result
        assert "<error_count>1</error_count>" in result
        assert "</batch>" in result
    
    def test_save_batch_xml_to_file(self):
        """Testa salvar batch em arquivo XML"""
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
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            XMLFormatter.save_batch_to_file(results, tmp_path)
            assert os.path.exists(tmp_path)
            
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "user1" in content
            assert "SUCCESS" in content or "true" in content
            
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_format_batch_empty_results(self):
        """Testa formatação de batch vazio"""
        results = []
        
        result = XMLFormatter.format_batch(results)
        
        assert "<batch>" in result
        assert "<total>0</total>" in result