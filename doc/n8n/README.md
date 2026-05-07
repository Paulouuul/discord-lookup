# n8n Automation Workflow

[![n8n](https://img.shields.io/badge/n8n-v2.19.4+-orange)](https://n8n.io/)
[![Slack](https://img.shields.io/badge/slack-webhook-blue)](https://slack.com/)
[![Google Sheets](https://img.shields.io/badge/google-sheets-green)](https://sheets.google.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](../../LICENSE)

## Prerequisites

Before importing this workflow, ensure you have:

| Requirement | Status | Notes |
|-------------|--------|-------|
| n8n running | ✅ Required | Docker or self-hosted, v2.19.4+ |
| Google Sheets account | ✅ Required | OAuth2 with spreadsheets scope |
| Slack workspace | ✅ Required | OAuth2 app with `chat:write` scope |
| Discord Lookup API | ✅ Required | Running on `http://discord-lookup-api:8000` |
| Docker Compose | ⚠️ Optional | For containerized n8n deployment |

## Workflow Overview

The workflow automates the process of querying Discord users, storing results, and sending real-time alerts.
```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌─────────────┐
│   Webhook    │ ──► │  HTTP Call   │ ──► │  Transform   │ ──► │   Google     │ ──► │    Slack    │
│  (Discord)   │     │    (API)     │     │    (Data)    │     │   Sheets     │     │    Alert    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘     └─────────────┘

```

## Features

| Feature | Description |
|---------|-------------|
| **Webhook Integration** | Receives `user_id` via POST request |
| **API Consumption** | Calls Discord Lookup API (GET /users/{id}) |
| **Data Processing** | Extracts and transforms user data with JavaScript |
| **Bot Detection** | Identifies bot accounts and triggers special alerts |
| **Persistence** | Stores search history in Google Sheets |
| **Real-time Alerts** | Sends formatted notifications to Slack channel |
| **Error Handling** | Validates inputs and handles API failures |

## Workflow Nodes

| Node Name | Function |
|-----------|----------|
| `Discord Lookup Webhook` | Receives incoming requests with `user_id` |
| `Fetch Discord User` | HTTP Request to API endpoint |
| `Transform User Data` | JavaScript code node for data processing |
| `Save to Google Sheets` | Stores user data in spreadsheet |
| `Send Slack Alert` | Sends notification to #discord-alerts |

## Output Example in Slack

🔍 Consulta ao Discord API
```text
• Usuário: enrico3509 (Enrico)
• ID: `561973026711797792`
• Status: 👤 Usuário Normal
• Criado em: 31/03/2019 18:00
• Consulta em: 2026-05-07T04:31:39.160Z
```
## Import and Configure

1. Import Workflow
```bash
# Access n8n UI
http://localhost:5678
# Workflows → Import from File
# Select: doc/n8n/discord-lookup-workflow.json
```
2. Configure Credentials
| Service | Configuration |
|---------|---------------|
| **Google Sheets** | OAuth2 with `https://www.googleapis.com/auth/spreadsheets` scope |
| **Slack** | OAuth2 with `chat:write` scope |
| **Discord API** | Base URL: `http://discord-lookup-api:8000` |
3. Set Up Webhook
```bash
## Test webhook (development)
curl -X POST http://localhost:5678/webhook-test/discord-lookup \
  -H "Content-Type: application/json" \
  -d '{"user_id": "561973026711797792"}'

## Production webhook (after activating workflow)

curl -X POST http://localhost:5678/webhook/discord-lookup \
  -H "Content-Type: application/json" \
  -d '{"user_id": "561973026711797792"}'
```

## Testing the Workflow
```bash
# 1. Start n8n
docker-compose -f docker-compose.n8n.yml up -d

# 2. Import workflow in n8n UI

# 3. Test with real user ID
curl -X POST http://localhost:5678/webhook-test/discord-lookup \
  -H "Content-Type: application/json" \
  -d '{"user_id": "561973026711797792"}'

# 4. Check Google Sheets for new row
# 5. Verify Slack channel for notification
```
### Workflow Version

| Property | Value |
|----------|-------|
| **Version** | 1.0.0 |
| **n8n Compatibility** | v2.19.4+ |
| **Last Updated** | May 2026 |
| **Author** | Paulo Ricardo Tebet Lyrio |

## File Location
doc/n8n/discord-lookup-workflow.json

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `N8N_HOST` | n8n host address | `localhost` |
| `N8N_PORT` | n8n port | `5678` |
| `WEBHOOK_URL` | Public webhook URL | `http://localhost:5678/` |

## Limitations
- Single user lookup only (batch processing not supported in this workflow)
- Requires Discord Lookup API to be running on `http://discord-lookup-api:8000`
- Webhook URL assumes n8n is accessible at `http://localhost:5678`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Webhook not responding | Check if workflow is Active (toggle in top-right) |
| "channel_not_found" error | Use Channel ID instead of channel name |
| Google Sheets auth fails | Re-authenticate OAuth2 credential |
| API connection refused | Verify Discord API container is running |

## Contributing
To modify this workflow:
1. Import the JSON file into n8n
2. Make your changes
3. Export as new JSON
4. Update documentation

## Related Documentation

- [n8n Workflow Documentation](https://docs.n8n.io/)
- [Slack Webhook API](https://api.slack.com/messaging/webhooks)
- [Google Sheets API](https://developers.google.com/sheets/api)