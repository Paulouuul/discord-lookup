import pytest
from unittest.mock import Mock, patch
from discord_lookup.client import DiscordClient

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
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    mock_get.side_effect = lambda *args, **kwargs: exec('raise requests.exceptions.HTTPError()')
    
    # Ou use pytest.raises