# ⚙️ Service Monitor
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![Notifications](https://img.shields.io/badge/Notifications-Telegram%20%7C%20Webhook-26A5E4)

🔗 Nav: [🎮 Steam](app/modules/steam/README.md) · [🤖 OpenAI](app/modules/openai/README.md) · [🟣 Claude](app/modules/claude/README.md) · [🧭 Cfx](app/modules/cfx/README.md) · [☁️ OCI](app/modules/oci/README.md) · [🌐 GCP](app/modules/gcp/README.md) · [☁️ AWS](app/modules/aws/README.md) · [🔔 Notifications](app/notifications/README.md) · [🐳 Docker](DOCKER.md)

Modular Python monitor that checks third-party status pages (Steam, OpenAI, Claude, Cfx, OCI, GCP, and AWS) and sends configurable notifications whenever any module enters ALERT.

## 📘 Structure
- `app/`: core, modules (`steam`, `openai`, `claude`, `cfx`, `oci`, `gcp`, `aws`), and notifiers.
- `docker-compose.yml`, `Dockerfile`, and `.env(.example)` live at the repo root to simplify local and container deployments.

## 📦 Modules
- 🎮 **Steam**: tracks https://steamstat.us/, applies `status`/`keyword`/`regex` rules over the “Steam Services” section, and reports which services are down. [app/modules/steam/README.md](app/modules/steam/README.md)
- 🤖 **OpenAI Status**: consumes `https://status.openai.com/api/v2/summary.json`, filters components/ids, and raises ALERTs for degraded incidents or outages. [app/modules/openai/README.md](app/modules/openai/README.md)
- 🟣 **Claude Status**: monitors `https://status.claude.com/api/v2/summary.json`, supports component filtering and `keyword/regex` filters. [app/modules/claude/README.md](app/modules/claude/README.md)
- 🧭 **Cfx Status**: consumes `https://status.cfx.re/api/v2/summary.json` to detect degraded/partial/major outages per component. [app/modules/cfx/README.md](app/modules/cfx/README.md)
- ☁️ **OCI Status (LAD)**: uses the RSS feed `https://ocistatus.oraclecloud.com/api/v2/incident-summary.rss`, monitoring LAD (default Brazil East/Brazil Southeast). [app/modules/oci/README.md](app/modules/oci/README.md)
- 🌐 **GCP Status (Americas)**: queries `https://status.cloud.google.com/incidents.json`, focused on regions `southamerica-east1`, `us-central1`, `us-east1`. [app/modules/gcp/README.md](app/modules/gcp/README.md)
- ☁️ **AWS Status**: fetches `https://health.aws.amazon.com/public/currentevents`, filters active events and regions `sa-east-1`, `us-east-1`, `us-east-2`. [app/modules/aws/README.md](app/modules/aws/README.md)

## 🔔 Notifications
The central `NotificationManager` dispatches enabled channels whenever a module goes to `ALERT` or a service returns to `OK`. The current implementation provides:
- **Telegram**: sends HTML cards (`Service-Checker — Alert/Resolved`) to one or more chats/groups. Configure `TELEGRAM_ENABLED=true`, `TELEGRAM_BOT_TOKEN`, and set `TELEGRAM_CHAT_ID` or `TELEGRAM_CHAT_IDS` (use negative IDs for groups). Adjust `TELEGRAM_TIMESTAMP_FORMAT` (default `%Y-%m-%d %H:%M:%S %Z`) and `TELEGRAM_TIMESTAMP_ZONE` (`UTC` or `LOCAL`) to control format and timezone. See [app/notifications/telegram/README.md](app/notifications/telegram/README.md) for validating the token via `getMe`, discovering the chat_id (e.g., send a message to the bot and use `https://api.telegram.org/bot$TOKEN/getUpdates`), and template structure details.
- **Webhook**: sends a JSON POST to `WEBHOOK_URL` with `ALERT` or `RESOLVED` events and optional `WEBHOOK_TOKEN`/`WEBHOOK_HEADER_NAME` authentication. See the [webhook README](app/notifications/webhook/README.md) for payload and examples.

## 🚀 Quick start
1. Update `.env` (or `.env.example`) with your keys and filters.
2. Run `docker compose up --build` in the repo root.
3. Check logs with `docker compose logs --tail 20` or `docker logs <container>`.

## 🧰 Configuration
- `SERVICE_MONITOR_MODULES` controls which modules are loaded (default `steam,openai,claude,cfx,oci,gcp,aws`).
- Each module respects `<PREFIX>_ENABLED` (default `true`), `<PREFIX>_RULE_*`, `<PREFIX>_SERVICE_FILTER`, and more.
- Enable notifications with `TELEGRAM_ENABLED=true` and/or `WEBHOOK_ENABLED=true`. If a notification fails, the monitor keeps running and logs the error.
- Control alert repeat cadence with `NOTIFICATION_REPEAT_MINUTES` (minutes; default `10`).
- For modules that return a list of services (Steam, OpenAI, etc.), the cycle is **per service**: alerts, repeats, and resolution are tracked individually.

## 🔗 Quick docs
- Modules: [Steam](app/modules/steam/README.md), [OpenAI](app/modules/openai/README.md), [Claude](app/modules/claude/README.md), [Cfx](app/modules/cfx/README.md), [OCI](app/modules/oci/README.md), [GCP](app/modules/gcp/README.md), [AWS](app/modules/aws/README.md)
- Notifications: [notifier overview](app/notifications/README.md) · [Telegram](app/notifications/telegram/README.md) · [Webhook](app/notifications/webhook/README.md)
- Infra: [DOCKER.md](DOCKER.md), [docker-compose.yml](docker-compose.yml)
