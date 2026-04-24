import pytest
from unittest.mock import Mock, patch
import requests
from discord_lookup.client import DiscordClient, DiscordAPIError


@patch('discord_lookup.client.requests.get')
def test_get_user_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "123", "username": "teste", "discriminator": "0000",
        "avatar": None, "bot": False, "public_flags": 0,
        "global_name": None, "banner": None
    }
    mock_get.return_value = mock_response
    
    client = DiscordClient("fake_token")
    user = client.get_user("123456789012345678")
    
    assert user.id == "123"
    assert user.username == "teste"


@patch('discord_lookup.client.requests.get')
def test_get_user_404(mock_get):
    """Testa erro 404 (usuário não encontrado)"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    # Configurar o mock para lançar HTTPError
    mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)
    
    client = DiscordClient("fake_token")
    
    with pytest.raises(ValueError, match="Usuário 123456789012345678 não encontrado"):
        client.get_user("123456789012345678")


@patch('discord_lookup.client.requests.get')
def test_get_user_401(mock_get):
    """Testa erro 401 (token inválido)"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_get.return_value = mock_response
    
    mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)
    
    client = DiscordClient("fake_token")
    
    with pytest.raises(ValueError, match="Token inválido"):
        client.get_user("123456789012345678")


@patch('discord_lookup.client.requests.get')
def test_get_user_rate_limit(mock_get):
    """Testa rate limiting (429)"""
    # Primeira chamada: rate limit (retorna status 429, SEM exceção)
    mock_response_429 = Mock()
    mock_response_429.status_code = 429
    mock_response_429.json.return_value = {"retry_after": 0.1}
    
    # Segunda chamada: sucesso
    mock_response_200 = Mock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        "id": "123", "username": "teste", "discriminator": "0000",
        "avatar": None, "bot": False, "public_flags": 0,
        "global_name": None, "banner": None
    }
    
    # Retorna as respostas diretamente (SEM HTTPError)
    mock_get.side_effect = [mock_response_429, mock_response_200]
    
    client = DiscordClient("fake_token")
    user = client.get_user("123456789012345678")
    
    assert user.id == "123"
    assert mock_get.call_count == 2

@patch('discord_lookup.client.requests.get')
def test_get_user_http_500(mock_get):
    """Testa erro HTTP 500 (Internal Server Error)"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_get.return_value = mock_response
    mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)
    
    client = DiscordClient("fake_token")
    
    with pytest.raises(DiscordAPIError, match="Erro HTTP 500"):
        client.get_user("123456789012345678")


@patch('discord_lookup.client.requests.get')
def test_get_user_timeout(mock_get):
    """Testa timeout"""
    mock_get.side_effect = requests.exceptions.Timeout
    
    client = DiscordClient("fake_token")
    
    with pytest.raises(DiscordAPIError, match="Timeout"):
        client.get_user("123456789012345678")


@patch('discord_lookup.client.requests.get')
def test_get_user_connection_error(mock_get):
    """Testa ConnectionError"""
    mock_get.side_effect = requests.exceptions.ConnectionError
    
    client = DiscordClient("fake_token")
    
    with pytest.raises(DiscordAPIError, match="Erro de conexão"):
        client.get_user("123456789012345678")
def test_invalid_user_id():
    """Testa validação de ID inválido"""
    client = DiscordClient("fake_token")
    
    with pytest.raises(ValueError, match="deve conter apenas números"):
        client.get_user("abc123")
    
    with pytest.raises(ValueError, match="deve ter entre 17 e 20 dígitos"):
        client.get_user("123")