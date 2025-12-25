# 🌐 GCP Status Module
![Module](https://img.shields.io/badge/Module-GCP-1F6FEB)
![Source](https://img.shields.io/badge/Source-status.cloud.google.com-0A66C2)

🔗 Nav: [🏠 Home](../../../README.md) · [🎮 Steam](../steam/README.md) · [🤖 OpenAI](../openai/README.md) · [🟣 Claude](../claude/README.md) · [🧭 Cfx](../cfx/README.md) · [☁️ OCI](../oci/README.md) · [☁️ AWS](../aws/README.md) · [🔔 Notifications](../../notifications/README.md) · [🐳 Docker](../../../DOCKER.md) · [📜 Spec](../../../openspec/changes/add-service-monitor-platform/specs/service-monitor/spec.md)

Monitor dos incidentes publicados em https://status.cloud.google.com (endpoint `incidents.json`), focado em regiões das Américas com filtro de regiões configurável.

## 📚 Documentação principal
- README geral: [../../../README.md](../../../README.md)
- Docker: [../../../DOCKER.md](../../../DOCKER.md)

## 🧭 Visão geral
- Busca `incidents.json` e avalia incidentes ativos (sem `end`) por região.
- Estratégias suportadas: `status` (padrão), `keyword`, `regex`.
- O ciclo de alerta e resolução é por incidente/região, com ALERT/RESOLVED independente.
- Filtro por regiões via `GCP_SERVICE_FILTER` (usa `id` das regiões, ex.: `us-east1`).

## 🔧 Variáveis de ambiente (`GCP_`)
- `URL` (default `https://status.cloud.google.com/incidents.json`)
- `INTERVAL_SECONDS` (default 60)
- `TIMEOUT_SECONDS` (default 10)
- `USER_AGENT` (default herdado ou `service-monitor/gcp`)
- `ENABLED`: `true/false` para ativar/desativar o módulo (default `true`)
- `RULE_KIND`: `status` (padrão), `keyword`, `regex`
- `RULE_VALUE`: para `status`, estados alvo (default `service_disruption,service_outage,service_information`); para `keyword`/`regex`, termo ou padrão
- `SERVICE_FILTER`: ids de regiões a monitorar (default `southamerica-east1,us-central1,us-east1`); vazio = todas

## 🚦 Regra `status`
- Considera incidentes sem campo `end` e com `status_impact` listado em `RULE_VALUE`.
- Gera ALERT se qualquer incidente ativo afetar alguma região filtrada.
- Payload inclui incidentes e regiões combinadas.

## 📇 Regiões monitoradas por padrão
- southamerica-east1 (São Paulo)
- us-central1 (Iowa)
- us-east1 (South Carolina)

💡 Para adicionar outra região, pegue o `id` exibido em `affected_locations` de `incidents.json`. Dica rápida:
```bash
curl -s https://status.cloud.google.com/incidents.json | jq -r '.[].affected_locations[]?.id' | sort -u
```
Coloque os ids desejados em `GCP_SERVICE_FILTER` separados por vírgula.

## ⚡ Exemplos rápidos
- Monitorar apenas as regiões padrão (default):
  - `GCP_RULE_KIND=status`
  - `GCP_RULE_VALUE=service_disruption,service_outage,service_information`
  - `GCP_SERVICE_FILTER=southamerica-east1,us-central1,us-east1`
- Monitorar só us-east1:
  - `GCP_SERVICE_FILTER=us-east1`
- Buscar qualquer termo nos incidentes:
  - `GCP_RULE_KIND=keyword`
  - `GCP_RULE_VALUE=maintenance`
