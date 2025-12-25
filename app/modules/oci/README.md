# ☁️ OCI Status Module
![Module](https://img.shields.io/badge/Module-OCI-1F6FEB)
![Source](https://img.shields.io/badge/Source-ocistatus.oraclecloud.com-0A66C2)

🔗 Nav: [🏠 Home](../../../README.md) · [🎮 Steam](../steam/README.md) · [🤖 OpenAI](../openai/README.md) · [🟣 Claude](../claude/README.md) · [🧭 Cfx](../cfx/README.md) · [🌐 GCP](../gcp/README.md) · [☁️ AWS](../aws/README.md) · [🔔 Notifications](../../notifications/README.md) · [🐳 Docker](../../../DOCKER.md) · [📜 Spec](../../../openspec/changes/add-service-monitor-platform/specs/service-monitor/spec.md)

Monitor do status da Oracle Cloud em https://ocistatus.oraclecloud.com via feed RSS `incident-summary.rss`, com foco nas regiões LAD.

## 📚 Documentação principal
- README geral: [../../../README.md](../../../README.md)
- Docker: [../../../DOCKER.md](../../../DOCKER.md)

## 🧭 Visão geral
- Faz GET no feed RSS de incidentes, extrai o status atual de cada item e aplica a regra configurada.
- Estratégias suportadas: `status` (padrão), `keyword`, `regex`.
- O ciclo de alerta e resolução é por item do feed (região/serviço), com ALERT/RESOLVED independente.
- Filtro de regiões/zones via `OCI_SERVICE_FILTER` (case-insensitive).

## 🔧 Variáveis de ambiente (`OCI_`)
- `URL` (default `https://ocistatus.oraclecloud.com/api/v2/incident-summary.rss`)
- `INTERVAL_SECONDS` (default 60)
- `TIMEOUT_SECONDS` (default 10)
- `USER_AGENT` (default herdado ou `service-monitor/oci`)
- `ENABLED`: `true/false` para ativar/desativar o módulo (default `true`)
- `RULE_KIND`: `status` (padrão), `keyword`, `regex`
- `RULE_VALUE`: para `status`, estados alvo (default `investigating,identified,monitoring`); para `keyword`/`regex`, termo ou padrão
- `SERVICE_FILTER`: regiões/zonas a monitorar (default `"Brazil East (Sao Paulo),Brazil Southeast (Vinhedo)"`); vazio = todas

## 🚦 Regra `status`
- Lê o primeiro `<strong>` do `description` de cada item como status atual (ex.: `Investigating`, `Identified`, `Monitoring`, `Resolved`).
- Gera ALERT se alguma região filtrada tiver status presente em `RULE_VALUE`.
- Payload retorna os incidentes avaliados ou somente os que geraram ALERT.

## 🌎 Regiões monitoradas por padrão
- Brazil East (Sao Paulo)
- Brazil Southeast (Vinhedo)

💡 Se precisar de outra região/serviço não listado, capture o nome exato exibido no título do feed e coloque em `OCI_SERVICE_FILTER` (separado por vírgula). Dica rápida para listar regiões recentes:
```bash
curl -s https://ocistatus.oraclecloud.com/api/v2/incident-summary.rss \
  | rg '<title>' | sed 's/.*<title>\\(.*\\)<\\/title>.*/\\1/' \
  | cut -d '|' -f2 | sed 's/^ *//;s/ *$//' | sort -u
```

## ⚡ Exemplos rápidos
- Monitorar apenas LAD (default):
  - `OCI_RULE_KIND=status`
  - `OCI_RULE_VALUE=investigating,identified,monitoring`
  - `OCI_SERVICE_FILTER="Brazil East (Sao Paulo),Brazil Southeast (Vinhedo)"`
- Monitorar qualquer incidente ativo na América do Norte:
  - `OCI_RULE_KIND=status`
  - `OCI_SERVICE_FILTER="us east,us west,canada"`
- Buscar padrão específico no feed:
  - `OCI_RULE_KIND=keyword`
  - `OCI_RULE_VALUE=maintenance`
