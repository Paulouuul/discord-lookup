import requests
import sys
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Cole seu BOT TOKEN aqui
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

def snowflake_to_timestamp(snowflake):
    """Converte Discord Snowflake ID em data de criação"""
    timestamp = (int(snowflake) >> 22) + 1420070400000
    return datetime.fromtimestamp(timestamp / 1000).strftime("%d/%m/%Y %H:%M")

def lookup_user(user_id):
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "User-Agent": "DiscordBot (https://github.com/seuuser/discord-lookup, 1.0)"
    }

    url = f"https://discord.com/api/v10/users/{user_id}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        print(f"✅ USUÁRIO ENCONTRADO!")
        print(f"ID: {data.get('id', 'N/A')}")
        print(f"Username: {data.get('username', 'N/A')}")
        print(f"Discriminator: #{data.get('discriminator', '0000')}")
        print(f"Nome Completo: {data.get('username', 'N/A')}#{data.get('discriminator', '0000')}")
        print(f"Avatar: https://cdn.discordapp.com/avatars/{data.get('id')}/{data.get('avatar')}.png?size=512")
        print(f"Bot: {'Sim' if data.get('bot') else 'Não'}")
        print(f"Data Criação: {snowflake_to_timestamp(data.get('id'))}")
        print(f"Badges/Flags: {data.get('public_flags', 0)}")
        print(f"Global Name: {data.get('global_name', 'N/A')}")

        if data.get('banner'):
            print(f"Banner: https://cdn.discordapp.com/banners/{data.get('id')}/{data.get('banner')}.png?size=512")

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print("❌ Usuário não encontrado ou ID inválido.")
        elif response.status_code == 401:
            print("❌ Token inválido. Verifique DISCORD_TOKEN.")
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 discord_user_lookup.py <USER_ID>")
        print("Ex: python3 discord_user_lookup.py 123456789012345678")
        sys.exit(1)

    user_id = sys.argv[1]
    lookup_user(user_id)