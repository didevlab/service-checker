# ☁️ AWS Status Module
![Module](https://img.shields.io/badge/Module-AWS-1F6FEB)
![Source](https://img.shields.io/badge/Source-health.aws.amazon.com-0A66C2)

🔗 Nav: [🏠 Home](../../../README.md) · [🎮 Steam](../steam/README.md) · [🤖 OpenAI](../openai/README.md) · [🟣 Claude](../claude/README.md) · [🧭 Cfx](../cfx/README.md) · [☁️ OCI](../oci/README.md) · [🌐 GCP](../gcp/README.md) · [🔔 Notifications](../../notifications/README.md) · [🐳 Docker](../../../DOCKER.md) · [📜 Spec](../../../openspec/changes/add-service-monitor-platform/specs/service-monitor/spec.md)

Monitor dos eventos públicos do AWS Health Dashboard em `https://health.aws.amazon.com/public/currentevents`, focado em regiões específicas.

## 📚 Documentação principal
- README geral: [../../../README.md](../../../README.md)
- Docker: [../../../DOCKER.md](../../../DOCKER.md)

## 🧭 Visão geral
- Consulta `currentevents` (JSON) e avalia eventos ativos (sem `endTime`) nas regiões selecionadas.
- Estratégias suportadas: `status` (padrão), `keyword`, `regex`.
- O ciclo de alerta e resolução é por evento/região, com ALERT/RESOLVED independente.
- Filtro por regiões via `AWS_SERVICE_FILTER` (ids como `us-east-1`).

## 🔧 Variáveis de ambiente (`AWS_`)
- `URL` (default `https://health.aws.amazon.com/public/currentevents`)
- `INTERVAL_SECONDS` (default 60)
- `TIMEOUT_SECONDS` (default 10)
- `USER_AGENT` (default herdado ou `service-monitor/aws`)
- `ENABLED`: `true/false` para ativar/desativar o módulo (default `true`)
- `RULE_KIND`: `status` (padrão), `keyword`, `regex`
- `RULE_VALUE`: para `status`, tokens a casar com `typeCode` dos eventos (default `operational_issue`); para `keyword`/`regex`, termo ou padrão aplicado ao JSON
- `SERVICE_FILTER`: ids de regiões a monitorar (default `sa-east-1,us-east-1,us-east-2`); vazio = todas

## 🚦 Regra `status`
- Considera eventos ativos (`endTime` ausente).
- Compara `typeCode` dos eventos com os tokens de `RULE_VALUE` (case-insensitive).
- Gera ALERT se houver evento ativo que afete qualquer região filtrada.

## 📇 Regiões monitoradas por padrão
- sa-east-1 (São Paulo)
- us-east-1 (N. Virginia)
- us-east-2 (Ohio)

💡 Para outras regiões, use o id exatamente como exibido em `region` nos eventos. Dica rápida:
```bash
curl -s https://health.aws.amazon.com/public/events | jq -r '.[].region' | sort -u | head
```

## ⚡ Exemplos rápidos
- Default (latam/US leste):
  - `AWS_RULE_KIND=status`
  - `AWS_RULE_VALUE=operational_issue`
  - `AWS_SERVICE_FILTER=sa-east-1,us-east-1,us-east-2`
- Monitorar apenas us-east-1:
  - `AWS_SERVICE_FILTER=us-east-1`
- Buscar termo livre:
  - `AWS_RULE_KIND=keyword`
  - `AWS_RULE_VALUE=latency`
