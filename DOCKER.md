# Service monitor docker usage

1. Update `.env` (already populated with defaults; use `.env.example` if you want to reset). The default Steam rule uses `STEAM_RULE_KIND=status` and checks severities `major,minor` in the “Steam Services” section; switch to `keyword`/`regex` if you want a different logic. Use `STEAM_SERVICE_FILTER` (comma-separated list) to monitor specific services by HTML `id` (e.g., `store,community,webapi`); empty means all.
2. Build and start: `docker compose up --build` (run from this folder). The build uses `requirements.txt` at the repo root.
3. Logs go to stdout. Defaults load the modules `steam` (HTML), `openai` (summary JSON), `claude` (summary JSON), `cfx` (summary JSON), `oci` (RSS), `gcp` (incidents JSON), and `aws` (current events JSON) every 60s.

Steam module variables (`STEAM_`):
- `STEAM_URL` (default `https://steamstat.us/`)
- `STEAM_RULE_KIND` (default `status`)
- `STEAM_RULE_VALUE` (default `major,minor`)
- `STEAM_SERVICE_FILTER` (service IDs; empty = all)
- `STEAM_ENABLED` (default `true`)

OpenAI module variables (`OPENAI_`):
- `OPENAI_URL` (default `https://status.openai.com/api/v2/summary.json`)
- `OPENAI_RULE_KIND` (default `status`)
- `OPENAI_RULE_VALUE` (default `degraded_performance,partial_outage,major_outage`)
- `OPENAI_SERVICE_FILTER` (component slugs/ids; empty = all)
- `OPENAI_ENABLED` (default `true`)

Claude module variables (`CLAUDE_`):
- `CLAUDE_URL` (default `https://status.claude.com/api/v2/summary.json`)
- `CLAUDE_RULE_KIND` (default `status`)
- `CLAUDE_RULE_VALUE` (default `degraded_performance,partial_outage,major_outage`)
- `CLAUDE_SERVICE_FILTER` (component slugs/ids; empty = all)
- `CLAUDE_ENABLED` (default `true`)

Cfx module variables (`CFX_`):
- `CFX_URL` (default `https://status.cfx.re/api/v2/summary.json`)
- `CFX_RULE_KIND` (default `status`)
- `CFX_RULE_VALUE` (default `degraded_performance,partial_outage,major_outage`)
- `CFX_SERVICE_FILTER` (component slugs/ids; empty = all)
- `CFX_ENABLED` (default `true`)

OCI module variables (`OCI_`):
- `OCI_URL` (default `https://ocistatus.oraclecloud.com/api/v2/incident-summary.rss`)
- `OCI_RULE_KIND` (default `status`)
- `OCI_RULE_VALUE` (default `investigating,identified,monitoring`)
- `OCI_SERVICE_FILTER` (regions/zones; default `Brazil East (Sao Paulo),Brazil Southeast (Vinhedo)`)
- `OCI_ENABLED` (default `true`)

GCP module variables (`GCP_`):
- `GCP_URL` (default `https://status.cloud.google.com/incidents.json`)
- `GCP_RULE_KIND` (default `status`)
- `GCP_RULE_VALUE` (default `service_disruption,service_outage,service_information`)
- `GCP_SERVICE_FILTER` (region ids; default `southamerica-east1,us-central1,us-east1`)
- `GCP_ENABLED` (default `true`)

AWS module variables (`AWS_`):
- `AWS_URL` (default `https://health.aws.amazon.com/public/currentevents`)
- `AWS_RULE_KIND` (default `status`)
- `AWS_RULE_VALUE` (default `operational_issue`)
- `AWS_SERVICE_FILTER` (region ids; default `sa-east-1,us-east-1,us-east-2`)
- `AWS_ENABLED` (default `true`)

Notifications (Telegram):
- `TELEGRAM_ENABLED` (default `false`)
- `TELEGRAM_BOT_TOKEN` (required when enabled)
- `TELEGRAM_CHAT_ID` (private chat or group; ignored if `TELEGRAM_CHAT_IDS` is set)
- `TELEGRAM_CHAT_IDS` (comma-separated list for multiple chats/groups; use negative IDs for groups)
- `TELEGRAM_API_URL` (default `https://api.telegram.org`)

Notifications (Webhook):
- `WEBHOOK_ENABLED` (default `false`)
- `WEBHOOK_URL` (target endpoint; required when enabled)
- `WEBHOOK_TOKEN` (optional; sent in a header)
- `WEBHOOK_HEADER_NAME` (default `Authorization`)
- `NOTIFICATION_REPEAT_MINUTES` (minutes between alert repeats while an incident persists; default `10`)

Enable/disable toggles:
- `STEAM_ENABLED`, `OPENAI_ENABLED`, `CLAUDE_ENABLED`, `CFX_ENABLED`, `OCI_ENABLED`, `GCP_ENABLED`, `AWS_ENABLED` (default `true`)

Key environment knobs:
- `SERVICE_MONITOR_MODULES`: comma list of module slugs to load (default `steam,openai,claude,cfx,oci,gcp,aws`).
- `SERVICE_MONITOR_DEFAULT_*`: fallback interval/timeout/user-agent used when module-specific envs are absent.
- `STEAM_RULE_KIND` / `STEAM_RULE_VALUE`: set `keyword` or `regex` matching against the steamstat.us HTML; a match yields an ALERT.

To simulate a local alert, set `STEAM_RULE_VALUE` to a word that exists or use a regex that always matches (e.g., `.*`). Restart `docker compose up` and follow the logs to see an ALERT while the app keeps running.
