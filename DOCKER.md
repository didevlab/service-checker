# Docker usage

This guide focuses on running Service Monitor with Docker Compose and tuning it through environment variables.

## ✅ Prerequisites
- Docker Engine and Docker Compose v2
- A `.env` file at the repo root (start from `.env.example`)

## 🚀 Quick start
1. Copy the example env file:
   ```bash
   cp .env.example .env
   ```
2. Start the stack from the repository root:
   ```bash
   docker compose up --build
   ```
3. Follow logs:
   ```bash
   docker compose logs --tail 50 -f
   ```

## 🧭 How it works
- Each module runs on a schedule (default 60s) and pulls a provider status source.
- Rules decide when a module emits `ALERT` or `RESOLVED`.
- Notifications are dispatched via Telegram or Webhook when enabled.

## 🧰 Global configuration
These apply across modules:
- `SERVICE_MONITOR_MODULES`: comma-separated list of module slugs to load (default `steam,openai,claude,cfx,oci,gcp,aws`).
- `SERVICE_MONITOR_DEFAULT_INTERVAL_SECONDS`: default polling interval in seconds.
- `SERVICE_MONITOR_DEFAULT_TIMEOUT_SECONDS`: default HTTP timeout in seconds.
- `SERVICE_MONITOR_DEFAULT_USER_AGENT`: default user-agent used by all modules.
- `NOTIFICATION_REPEAT_MINUTES`: minimum minutes between repeated alerts for the same service.

## 🔧 Module configuration
Each module supports the same environment shape:
- `<MODULE>_URL`
- `<MODULE>_RULE_KIND` (`status` | `keyword` | `regex`)
- `<MODULE>_RULE_VALUE` (rule target values)
- `<MODULE>_SERVICE_FILTER` (comma-separated IDs/slugs; empty = all)
- `<MODULE>_ENABLED` (`true` | `false`)

### Default module values
**Steam (`STEAM_`)**
- `STEAM_URL`: `https://steamstat.us/`
- `STEAM_RULE_KIND`: `status`
- `STEAM_RULE_VALUE`: `major,minor`
- `STEAM_SERVICE_FILTER`: empty (all)

**OpenAI (`OPENAI_`)**
- `OPENAI_URL`: `https://status.openai.com/api/v2/summary.json`
- `OPENAI_RULE_KIND`: `status`
- `OPENAI_RULE_VALUE`: `degraded_performance,partial_outage,major_outage`
- `OPENAI_SERVICE_FILTER`: empty (all)

**Claude (`CLAUDE_`)**
- `CLAUDE_URL`: `https://status.claude.com/api/v2/summary.json`
- `CLAUDE_RULE_KIND`: `status`
- `CLAUDE_RULE_VALUE`: `degraded_performance,partial_outage,major_outage`
- `CLAUDE_SERVICE_FILTER`: empty (all)

**Cfx (`CFX_`)**
- `CFX_URL`: `https://status.cfx.re/api/v2/summary.json`
- `CFX_RULE_KIND`: `status`
- `CFX_RULE_VALUE`: `degraded_performance,partial_outage,major_outage`
- `CFX_SERVICE_FILTER`: empty (all)

**OCI (`OCI_`)**
- `OCI_URL`: `https://ocistatus.oraclecloud.com/api/v2/incident-summary.rss`
- `OCI_RULE_KIND`: `status`
- `OCI_RULE_VALUE`: `investigating,identified,monitoring`
- `OCI_SERVICE_FILTER`: `Brazil East (Sao Paulo),Brazil Southeast (Vinhedo)`

**GCP (`GCP_`)**
- `GCP_URL`: `https://status.cloud.google.com/incidents.json`
- `GCP_RULE_KIND`: `status`
- `GCP_RULE_VALUE`: `service_disruption,service_outage,service_information`
- `GCP_SERVICE_FILTER`: `southamerica-east1,us-central1,us-east1`

**AWS (`AWS_`)**
- `AWS_URL`: `https://health.aws.amazon.com/public/currentevents`
- `AWS_RULE_KIND`: `status`
- `AWS_RULE_VALUE`: `operational_issue`
- `AWS_SERVICE_FILTER`: `sa-east-1,us-east-1,us-east-2`

## 🔔 Notifications
**Telegram**
- `TELEGRAM_ENABLED` (default `false`)
- `TELEGRAM_BOT_TOKEN` (required when enabled)
- `TELEGRAM_CHAT_ID` (single chat/group)
- `TELEGRAM_CHAT_IDS` (comma-separated list for multiple chats/groups)
- `TELEGRAM_API_URL` (default `https://api.telegram.org`)

**Webhook**
- `WEBHOOK_ENABLED` (default `false`)
- `WEBHOOK_URL` (required when enabled)
- `WEBHOOK_TOKEN` (optional)
- `WEBHOOK_HEADER_NAME` (default `Authorization`)

## 🧪 Simulate an alert
To force a local alert using Steam:
1. Set `STEAM_RULE_KIND=keyword` and `STEAM_RULE_VALUE=.*` (regex that always matches).
2. Restart the stack:
   ```bash
   docker compose up --build
   ```
3. Watch logs for the `ALERT` event.

## 🧯 Troubleshooting
- **No logs**: ensure the container is running and check `docker compose ps`.
- **No alerts**: confirm the module is enabled and the rule values are valid.
- **Telegram not sending**: verify token and chat ID; add the bot to the group.
- **Webhook failures**: confirm the endpoint is reachable and accepts JSON.
