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
- **Multiple output formats** - Table (colorful), JSON, and CSV
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
### Build the image
```bash
docker build -f Dockerfile.cli -t discord-lookup-cli .
```
### Run with volume for .env access
```bash
docker run --rm -v "$(pwd):/app" discord-lookup-cli USER_ID
```

## Usage

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
│       └── ci.yml          # GitHub Actions CI/CD
├── discord_lookup/         # Main package
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── client.py           # Discord API client
│   ├── formatters.py       # JSON and CSV formatters
│   ├── models.py           # Data models
│   └── utils.py            # Utility functions
├── tests/                  # Unit tests
│   ├── __init__.py
│   ├── test_client.py
│   ├── test_formatters.py
│   ├── test_models.py
│   └── test_utils.py
├── .dockerignore           # Docker ignore file
├── .gitignore              # Git ignore file
├── .Dockerfile.cli         # Docker configuration
├── README.md               # This file
└── requirements.txt        # Python dependencies
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
