import pytest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestAPI:
    """Testes para a API com mocks"""
    
    def test_health_check(self):
        """Testa endpoint /health (não precisa de mock)"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    
    @patch('discord_lookup.client.DiscordClient.get_user')
    def test_get_user_success(self, mock_get_user):
        """Testa busca de usuário com sucesso usando mock"""
        # Criar mock do usuário
        mock_user = Mock()
        mock_user.id = "123456789012345678"
        mock_user.username = "usuário_teste"
        mock_user.discriminator = "1234"
        mock_user.global_name = "Test User"
        mock_user.avatar_url = "https://cdn.discordapp.com/avatars/123456789012345678/avatar.png?size=512"
        mock_user.banner_url = None
        mock_user.is_bot = False
        mock_user.created_at = "01/01/2021 12:00"
        mock_user.public_flags = 0
        
        mock_get_user.return_value = mock_user
        
        response = client.get("/users/123456789012345678")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "123456789012345678"
        assert data["username"] == "usuário_teste"
        assert data["global_name"] == "Test User"
    
    @patch('discord_lookup.client.DiscordClient.get_user')
    def test_get_user_not_found(self, mock_get_user):
        """Testa usuário não encontrado"""
        mock_get_user.side_effect = ValueError("Usuário 999999999999999999 não encontrado")
        
        response = client.get("/users/999999999999999999")
        
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]
    
    @patch('discord_lookup.client.DiscordClient.get_users_batch')
    def test_batch_success(self, mock_get_batch):
        """Testa batch com sucesso usando mock"""
        # Mock do resultado do batch
        mock_get_batch.return_value = [
            {
                "user_id": "123456789012345678",
                "success": True,
                "data": {
                    "id": "123456789012345678",
                    "username": "usuario1",
                    "discriminator": "1234",
                    "global_name": "Nome Um",
                    "avatar_url": "https://example.com/avatar1.png",
                    "banner_url": None,
                    "created_at": "01/01/2021 12:00",
                    "is_bot": False,
                    "public_flags": 0
                }
            },
            {
                "user_id": "876543210987654321",
                "success": True,
                "data": {
                    "id": "876543210987654321",
                    "username": "usuario2",
                    "discriminator": "5678",
                    "global_name": "Nome Dois",
                    "avatar_url": "https://example.com/avatar2.png",
                    "banner_url": None,
                    "created_at": "15/03/2022 18:30",
                    "is_bot": False,
                    "public_flags": 0
                }
            }
        ]
        
        response = client.post(
            "/users/batch",
            json={"user_ids": ["123456789012345678", "876543210987654321"]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert data["success_count"] == 2
        assert data["error_count"] == 0
    
    @patch('discord_lookup.client.DiscordClient.get_user')
    def test_batch_with_invalid_id(self, mock_get_user):
        """Testa batch com ID inválido (cai na exceção)"""
        mock_get_user.side_effect = ValueError("ID inválido: 'invalid_id' - deve conter apenas números")
        
        response = client.post(
            "/users/batch",
            json={"user_ids": ["invalid_id"]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success_count"] == 0
        assert data["error_count"] == 1
    
    def test_batch_empty_request(self):
        """Testa batch com lista vazia"""
        response = client.post("/users/batch", json={"user_ids": []})
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
    
    @patch('discord_lookup.client.DiscordClient.get_user')
    def test_invalid_accept_header(self, mock_get_user):
        """Testa Accept header inválido (deve retornar JSON)"""
        # Mock do usuário
        mock_user = Mock()
        mock_user.id = "123456789012345678"
        mock_user.username = "testuser"
        mock_user.discriminator = "0000"
        mock_user.global_name = None
        mock_user.avatar_url = "https://example.com/avatar.png"
        mock_user.banner_url = None
        mock_user.is_bot = False
        mock_user.created_at = "01/01/2021 12:00"
        mock_user.public_flags = 0
        
        mock_get_user.return_value = mock_user
        
        response = client.get(
            "/users/123456789012345678",
            headers={"Accept": "application/invalid"}
        )
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"