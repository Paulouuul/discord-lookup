from discord_lookup.models import DiscordUser

def test_discord_user_avatar_url():
    user = DiscordUser(
        id="123", username="teste", discriminator="0000",
        avatar="abc123", bot=False
    )
    assert "abc123" in user.avatar_url
    assert "123" in user.avatar_url

def test_discord_user_is_bot():
    user = DiscordUser(id="123", username="teste", discriminator="0000", avatar=None)
    assert user.is_bot is False
    
    bot_user = DiscordUser(id="456", username="bot", discriminator="0000", avatar=None, bot=True)
    assert bot_user.is_bot is True