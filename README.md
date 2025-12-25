# ⚙️ Service Monitor
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![Notifications](https://img.shields.io/badge/Notifications-Telegram%20%7C%20Webhook-26A5E4)

🔗 Nav: [🎮 Steam](app/modules/steam/README.md) · [🤖 OpenAI](app/modules/openai/README.md) · [🟣 Claude](app/modules/claude/README.md) · [🧭 Cfx](app/modules/cfx/README.md) · [☁️ OCI](app/modules/oci/README.md) · [🌐 GCP](app/modules/gcp/README.md) · [☁️ AWS](app/modules/aws/README.md) · [🔔 Notifications](app/notifications/README.md) · [🐳 Docker](DOCKER.md)

A modular Python monitor that continuously checks third-party status pages (Steam, OpenAI, Claude, Cfx, OCI, GCP, and AWS) and sends configurable alerts when any module detects an incident.

## ✅ Highlights
- Modular, plug-in style monitors for popular status providers.
- Multiple notification channels (Telegram, Webhook).
- Per-service alert lifecycle with repeat throttling.
- Docker-first deployment with sensible defaults.

## 🧱 Project structure
- `app/`: core engine, module loaders, modules, and notifiers.
- `docker-compose.yml`, `Dockerfile`, and `.env(.example)`: local and container runtime.

## 📦 Modules
Each module pulls a provider-specific status source and applies rules configured via environment variables.

- 🎮 **Steam**: https://steamstat.us/ (HTML parsing with status/keyword/regex).
- 🤖 **OpenAI**: https://status.openai.com (`/api/v2/summary.json`).
- 🟣 **Claude**: https://status.claude.com (`/api/v2/summary.json`).
- 🧭 **Cfx**: https://status.cfx.re (`/api/v2/summary.json`).
- ☁️ **OCI**: https://ocistatus.oraclecloud.com (RSS `incident-summary.rss`).
- 🌐 **GCP**: https://status.cloud.google.com (`incidents.json`).
- ☁️ **AWS**: https://health.aws.amazon.com/public/currentevents (JSON events).

See each module README for rules, filters, and examples.

## 🔔 Notifications
Alerts are managed by `NotificationManager` and dispatched when a module reports `ALERT` or when a service returns to `OK`.

- **Telegram**: HTML card notifications for chats or groups.
- **Webhook**: JSON POST payloads for custom integrations.

## 🚀 Quick start
1. Copy `.env.example` to `.env` and customize filters/tokens.
2. Run `docker compose up --build` from the repository root.
3. Monitor logs with `docker compose logs --tail 20`.

## 🧰 Configuration essentials
- `SERVICE_MONITOR_MODULES`: comma-separated list of module slugs to load.
- `NOTIFICATION_REPEAT_MINUTES`: minimum interval to repeat alerts for the same service.
- `TELEGRAM_ENABLED` / `WEBHOOK_ENABLED`: enable channels.

Each module also supports its own `*_RULE_KIND`, `*_RULE_VALUE`, and `*_SERVICE_FILTER` keys.

## 🐳 Docker usage
See `DOCKER.md` for full environment reference, examples, and testing guidance.

## 🔗 Documentation
- Modules: [Steam](app/modules/steam/README.md), [OpenAI](app/modules/openai/README.md), [Claude](app/modules/claude/README.md), [Cfx](app/modules/cfx/README.md), [OCI](app/modules/oci/README.md), [GCP](app/modules/gcp/README.md), [AWS](app/modules/aws/README.md)
- Notifications: [Overview](app/notifications/README.md) · [Telegram](app/notifications/telegram/README.md) · [Webhook](app/notifications/webhook/README.md)
- Infra: [DOCKER.md](DOCKER.md), [docker-compose.yml](docker-compose.yml)
