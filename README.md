# Discord Lookup Tool

[![CI](https://github.com/Paulouuul/discord-lookup/actions/workflows/ci.yml/badge.svg)](https://github.com/Paulouuul/discord-lookup/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-supported-blue)](https://www.docker.com/)

## Description

Discord Lookup Tool is a command-line interface (CLI) application and Python library for querying user information from Discord's official API. It provides detailed user profiles including avatar, banner, account creation date, badges, and more.

## Features

- **User lookup by ID** - Get complete user information from Discord
- **Batch processing** - Process multiple user IDs from a file with progress bar
- **Multiple output formats** - - Table (colorful), JSON, CSV, YAML, HTML, XML, Markdown
- **Professional logging** - DEBUG, INFO, WARNING, ERROR levels with --verbose flag
- **Error handling** - Comprehensive error handling for API errors, rate limiting, and network issues
- **Docker support** - Containerized application for easy deployment
- **CI/CD** - Automated testing with GitHub Actions

## Technologies

- Python 3.10+
- Requests library for HTTP calls
- Colorama for terminal colors
- TQDM for progress bars
- Pytest for unit testing
- Docker for containerization
- GitHub Actions for CI/CD
- FastAPI for REST API
- Redis for caching

## Installation

### Local Installation

```bash
# Clone the repository
git clone https://github.com/Paulouuul/discord-lookup.git
cd discord-lookup

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your bot token
echo DISCORD_BOT_TOKEN=your_token_here > .env
```

## Docker Installation

### Build the CLI image
```bash
docker build -f Dockerfile.cli -t discord-lookup-cli .
```

### Build the API image
```bash
docker build -f Dockerfile.api -t discord-lookup-api
```

### Run the API with Docker Compose
```bash
docker-compose -f docker-compose.api.yml up -d
```

### Run with volume for .env access
```bash
docker run --rm -v "$(pwd):/app" discord-lookup-cli USER_ID
```

## CLI Usage

### Basic user lookup (table format)
```bash
python -m discord_lookup.cli USER_ID
```
### JSON output
```bash
python -m discord_lookup.cli USER_ID --output json
```
### CSV output
```bash
python -m discord_lookup.cli USER_ID --output csv
```
### Save output to file
```bash
python -m discord_lookup.cli USER_ID --output json --save output.json
```
### Batch processing
```bash
python -m discord_lookup.cli --batch ids.txt
```
### Batch with JSON output and save
```bash
python -m discord_lookup.cli --batch ids.txt --output json --save results.json
```
### Verbose mode (debug logs)
```bash
python -m discord_lookup.cli USER_ID --verbose
```
### Disable colors
```bash
python -m discord_lookup.cli USER_ID --no-color
```

## API Usage

### Start the API server

```bash
uvicorn api.main:app --reload --port 8000
```

### API Endpoints

| Method | Endpoint | Description | Formats |
|--------|----------|-------------|---------|
| GET | `/users/{id}` | Get user information | JSON, CSV, YAML, HTML, XML, Markdown |
| POST | `/users/batch` | Get multiple users | JSON, CSV, YAML, HTML, XML, Markdown |
| GET | `/health` | Health check | JSON |
| GET | `/docs` | Swagger documentation | HTML |

### API Examples

```bash
# JSON (default)
curl http://localhost:8000/users/561973026711797792

# CSV
curl -H "Accept: text/csv" http://localhost:8000/users/561973026711797792

# YAML
curl -H "Accept: application/x-yaml" http://localhost:8000/users/561973026711797792

# HTML
curl -H "Accept: text/html" http://localhost:8000/users/561973026711797792

# XML
curl -H "Accept: application/xml" http://localhost:8000/users/561973026711797792

# Markdown
curl -H "Accept: text/markdown" http://localhost:8000/users/561973026711797792

# Batch request
curl -X POST http://localhost:8000/users/batch \
  -H "Content-Type: application/json" \
  -d '{"user_ids": ["561973026711797792", "563529796768759840"]}'
```
### Redis Cache

The API uses Redis for caching with 1-hour TTL to improve performance.

**Clear cache:**
```bash
docker exec discord-lookup-redis-1 redis-cli FLUSHALL
```

**Check cache status:**
```bash
docker exec discord-lookup-redis-1 redis-cli DBSIZE
```
## n8n Automation

This project includes a complete n8n automation workflow that integrates the Discord Lookup API with Google Sheets and Slack.

The workflow:
- Receives `user_id` via webhook
- Queries the Discord Lookup API
- Stores results in Google Sheets
- Sends formatted alerts to Slack

📁 **Full documentation**: [doc/n8n/README.md](doc/n8n/README.md)

## Output Examples

### Table Format

```
2026-04-20 19:58:43,191 - INFO - Buscando usuário: 123456789012345678
2026-04-20 19:58:43,515 - INFO - USUARIO ENCONTRADO!
ID: 123456789012345678
Username: exemplo_usuario
Discriminator: #1234
Nome Completo: exemplo_usuario#1234
Avatar: https://cdn.discordapp.com/avatars/123456789012345678/avatar_hash.png?size=512
Bot: Nao
Data Criacao: 01/01/2021 12:00
Badges/Flags: 131072
Global Name: Exemplo Nome
```

### JSON Format

```json
{
  "id": "123456789012345678",
  "username": "exemplo_usuario",
  "discriminator": "1234",
  "global_name": "Exemplo Nome",
  "avatar_url": "https://cdn.discordapp.com/avatars/123456789012345678/avatar_hash.png?size=512",
  "banner_url": null,
  "is_bot": false,
  "created_at": "01/01/2021 12:00",
  "public_flags": 131072
}
```

### CSV Format

```csv
id,username,discriminator,global_name,avatar_url,banner_url,is_bot,created_at,public_flags
123456789012345678,exemplo_usuario,1234,Exemplo Nome,https://cdn.discordapp.com/avatars/123456789012345678/avatar_hash.png?size=512,,False,01/01/2021 12:00,131072
```

### Batch Output (JSON)

```json
{
  "total": 2,
  "success_count": 2,
  "error_count": 0,
  "results": [
    {
      "user_id": "123456789012345678",
      "success": true,
      "data": {
        "id": "123456789012345678",
        "username": "usuario1",
        "discriminator": "1234",
        "global_name": "Nome Um",
        "avatar_url": "https://cdn.discordapp.com/avatars/123456789012345678/avatar_hash.png?size=512",
        "banner_url": null,
        "is_bot": false,
        "created_at": "01/01/2021 12:00",
        "public_flags": 131072
      }
    },
    {
      "user_id": "876543210987654321",
      "success": true,
      "data": {
        "id": "876543210987654321",
        "username": "usuario2",
        "discriminator": "5678",
        "global_name": "Nome Dois",
        "avatar_url": "https://cdn.discordapp.com/avatars/876543210987654321/avatar_hash.png?size=512",
        "banner_url": null,
        "is_bot": false,
        "created_at": "15/03/2022 18:30",
        "public_flags": 0
      }
    }
  ]
}
```

### Batch Output (CSV)

```csv
user_id,success,username,discriminator,global_name,avatar_url,banner_url,is_bot,created_at,public_flags,error
123456789012345678,SUCCESS,usuario1,1234,Nome Um,https://cdn.discordapp.com/avatars/123456789012345678/avatar_hash.png?size=512,,False,01/01/2021 12:00,131072,
876543210987654321,SUCCESS,usuario2,5678,Nome Dois,https://cdn.discordapp.com/avatars/876543210987654321/avatar_hash.png?size=512,,False,15/03/2022 18:30,0,
```
## Help
```bash
python -m discord_lookup.cli --help
```

## As Python Library

```python
from discord_lookup import DiscordClient

client = DiscordClient(token="your_bot_token")
user = client.get_user("123456789012345678")
print(user.username)
print(user.created_at)

```

## Configuration
### 1. Getting a Discord Bot Token

Follow these steps to obtain a Discord bot token:

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click on "New Application" and give it a name
3. Go to the "Bot" tab in the left sidebar
4. Click "Add Bot" and confirm
5. Under the "Token" section, click "Copy" to copy your bot token
6. Enable the following Privileged Gateway Intents if needed:
   - Server Members Intent (for member information)
   - Message Content Intent (for message processing)

**Important:** Keep your token secure. Never share it or commit it to version control.

### 2. Create a `.env` file in the project root:
```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

## Project Structure

```
discord-lookup/
├── .github/
│   └── workflows/
│       └── ci.yml                     # GitHub Actions CI/CD pipeline (58 tests, Docker builds)
├── api/                               # FastAPI REST API module
│   ├── __init__.py
│   ├── config.py                      # API configuration (Redis, CORS, rate limiting)
│   ├── main.py                        # FastAPI application entry point
│   ├── router.py                      # API route definitions (/users, /health)
│   ├── cache/
│   │   ├── __init__.py
│   │   └── redis_cache.py             # Redis client with TTL and connection pooling
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── cache.py                   # Dependency injection for Redis cache
│   │   └── discord_client.py          # Dependency injection for Discord client
│   ├── models/
│   │   ├── __init.py__
│   │   └── schemas.py                 # Pydantic models (UserResponse, BatchResponse, etc.)
│   ├── use_cases/
│   │   ├── __init__.py
│   │   └── users/
│   │       ├── __init__.py
│   │       ├── get_user.py            # Single user business logic with cache
│   │       └── get_users_batch.py     # Batch users business logic with cache
│   └── utils/
│       ├── __init__.py
│       └── exporters.py               # Exporters for JSON, CSV, YAML, HTML, XML, Markdown
├── discord_lookup/                    # Main CLI package
│   ├── __init__.py
│   ├── cli.py                         # CLI entry point with argparse (7 output formats)
│   ├── client.py                      # Discord API client (rate limiting, error handling)
│   ├── models.py                      # DiscordUser dataclass (9 fields + properties)
│   ├── utils.py                       # Utilities (snowflake to timestamp conversion)
│   └── formatters/                    # Modular output formatters
│       ├── __init__.py
│       ├── base.py                    # BaseFormatter abstract class
│       ├── json_formatter.py          # JSON output (single + batch)
│       ├── csv_formatter.py           # CSV output (single + batch)
│       ├── yaml_formatter.py          # YAML output (single + batch)
│       ├── html_formatter.py          # HTML output with table and images
│       ├── xml_formatter.py           # XML output using dicttoxml
│       └── markdown_formatter.py      # Markdown output with table (11 columns)
│── doc/                               # Main CLI package
│   ├── images/                        # Screenshots
│   │   └── n8n/                       # n8n workflow screenshots
│           └── workflow-overview.png  # Complete workflow visualization
│   └── n8n/                           # n8n workflow documentation
│       ├── README.md                  # Complete n8n workflow guide
│       └── discord-lookup-workflow.json # n8n workflow export
├── tests/                             # Unit tests
│   ├── __init__.py
│   ├── test_cache.py                  # Redis cache tests
│   ├── test_client.py                 # DiscordClient tests
│   ├── test_csv_formatter.py          # CSVFormatter tests
│   ├── test_html_formatter.py         # HTMLFormatter tests
│   ├── test_json_formatter.py         # JSONFormatter tests
│   ├── test_markdown_formatter.py     # MarkdownFormatter tests
│   ├── test_models.py                 # DiscordUser model tests
│   ├── test_utils.py                  # Utils tests
│   ├── test_xml_formatter.py          # XMLFormatter tests
│   └── test_yaml_formatter.py         # YAMLFormatter tests
├── Dockerfile.cli                     # Docker image for CLI (python:3.11-slim)
├── Dockerfile.api                     # Docker image for API (python:3.11-slim + uvicorn)
├── docker-compose.api.yml             # Docker Compose (API + Redis services)
├── docker-compose.n8n.yml             # Docker Compose (N8N Service)
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```

## Running Tests
### Run all tests
```bash
pytest tests/ -v
```

### Run with coverage report
```bash
pytest tests/ --cov=discord_lookup --cov-report=term
```

### Run specific test file
```bash
pytest tests/test_formatters.py -v
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for full text.

## Author

**Paulo Ricardo Tebet Lyrio**

- GitHub: [@Paulouuul](https://github.com/Paulouuul)
- LinkedIn: [Paulo Ricardo Tebet Lyrio](https://www.linkedin.com/in/paulo-ricardo-tebet-lyrio-8258b619b)
- Email: tebetpaulo91@yahoo.com
