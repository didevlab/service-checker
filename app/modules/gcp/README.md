# 🌐 GCP Status Module
![Module](https://img.shields.io/badge/Module-GCP-1F6FEB)
![Source](https://img.shields.io/badge/Source-status.cloud.google.com-0A66C2)

🔗 Nav: [🏠 Home](../../../README.md) · [🎮 Steam](../steam/README.md) · [🤖 OpenAI](../openai/README.md) · [🟣 Claude](../claude/README.md) · [🧭 Cfx](../cfx/README.md) · [☁️ OCI](../oci/README.md) · [☁️ AWS](../aws/README.md) · [🔔 Notifications](../../notifications/README.md) · [🐳 Docker](../../../DOCKER.md)

Monitor incidents published at https://status.cloud.google.com (endpoint `incidents.json`), focused on Americas regions with configurable region filtering.

## 📚 Main docs
- General README: [../../../README.md](../../../README.md)
- Docker: [../../../DOCKER.md](../../../DOCKER.md)

## 🧭 Overview
- Fetches `incidents.json` and evaluates active incidents (no `end`) by region.
- Supported strategies: `status` (default), `keyword`, `regex`.
- Alert/resolution lifecycle is per incident/region, with independent ALERT/RESOLVED.
- Region filter via `GCP_SERVICE_FILTER` (uses region `id`, e.g., `us-east1`).

## 🔧 Environment variables (`GCP_`)
- `URL` (default `https://status.cloud.google.com/incidents.json`)
- `INTERVAL_SECONDS` (default 60)
- `TIMEOUT_SECONDS` (default 10)
- `USER_AGENT` (default inherited or `service-monitor/gcp`)
- `ENABLED`: `true/false` to enable/disable the module (default `true`)
- `RULE_KIND`: `status` (default), `keyword`, `regex`
- `RULE_VALUE`: for `status`, target states (default `service_disruption,service_outage,service_information`); for `keyword`/`regex`, a term or pattern
- `SERVICE_FILTER`: region ids to monitor (default `southamerica-east1,us-central1,us-east1`); empty = all

## 🚦 `status` rule
- Considers incidents without `end` and with `status_impact` listed in `RULE_VALUE`.
- Raises ALERT if any active incident affects a filtered region.
- Payload includes incidents and combined regions.

## 📇 Default monitored regions
- southamerica-east1 (Sao Paulo)
- us-central1 (Iowa)
- us-east1 (South Carolina)

💡 To add another region, take the `id` shown in `affected_locations` from `incidents.json`. Quick listing:
```bash
curl -s https://status.cloud.google.com/incidents.json | jq -r '.[].affected_locations[]?.id' | sort -u
```
Set the desired ids in `GCP_SERVICE_FILTER` separated by commas.

## ⚡ Quick examples
- Monitor only the default regions:
  - `GCP_RULE_KIND=status`
  - `GCP_RULE_VALUE=service_disruption,service_outage,service_information`
  - `GCP_SERVICE_FILTER=southamerica-east1,us-central1,us-east1`
- Monitor only us-east1:
  - `GCP_SERVICE_FILTER=us-east1`
- Search for any term in incidents:
  - `GCP_RULE_KIND=keyword`
  - `GCP_RULE_VALUE=maintenance`
