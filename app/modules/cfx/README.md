# 🧭 Cfx Status Module
![Module](https://img.shields.io/badge/Module-Cfx-1F6FEB)
![Source](https://img.shields.io/badge/Source-status.cfx.re-0A66C2)

🔗 Nav: [🏠 Home](../../../README.md) · [🎮 Steam](../steam/README.md) · [🤖 OpenAI](../openai/README.md) · [🟣 Claude](../claude/README.md) · [☁️ OCI](../oci/README.md) · [🌐 GCP](../gcp/README.md) · [☁️ AWS](../aws/README.md) · [🔔 Notifications](../../notifications/README.md) · [🐳 Docker](../../../DOCKER.md) · [📜 Spec](../../../openspec/changes/add-service-monitor-platform/specs/service-monitor/spec.md)

Monitor da página https://status.cfx.re usando o endpoint JSON `api/v2/summary.json`.

## 📚 Documentação principal
- README geral: [../../../README.md](../../../README.md)
- Docker: [../../../DOCKER.md](../../../DOCKER.md)

## 🧭 Visão geral
- Faz GET no summary JSON e avalia componentes por status.
- Estratégias suportadas: `status` (padrão), `keyword`, `regex`.
- O ciclo de alerta e resolução é por componente (cada `id`/`slug` gera ALERT/RESOLVED independente).
- Payload inclui os componentes avaliados (ou filtrados).

## 🔧 Variáveis de ambiente (`CFX_`)
- `URL` (default `https://status.cfx.re/api/v2/summary.json`)
- `INTERVAL_SECONDS` (default 60)
- `TIMEOUT_SECONDS` (default 10)
- `USER_AGENT` (default herdado ou `service-monitor/cfx`)
- `ENABLED`: `true/false` para ativar/desativar o módulo (default `true`)
- `RULE_KIND`: `status` (padrão), `keyword`, `regex`
- `RULE_VALUE`: para `status`, estados alvo (ex.: `degraded_performance,partial_outage,major_outage`); para `keyword`/`regex`, termo ou padrão
- `SERVICE_FILTER`: ids ou slugs de componentes a monitorar (ex.: `fivem,redm,keymaster`); vazio = todos

## 🚦 Regra `status`
- Usa os estados do statuspage (`operational`, `degraded_performance`, `partial_outage`, `major_outage`, `under_maintenance`).
- Gera ALERT se algum componente filtrado tiver status presente em `RULE_VALUE`.

### 📇 Componentes conhecidos (slug → nome)
- `cnl` → CnL (Client authentication)
- `forums` → Forums
- `games` (grupo) → Games
- `fivem` → FiveM
- `game-services` (grupo) → Game Services
- `policy` → Policy
- `server-list-frontend` → Server List Frontend
- `redm` → RedM
- `web-services` (grupo) → Web Services
- `keymaster` → Keymaster
- `runtime` → "Runtime"
- `cfx-re-platform-server-fxserver` → Cfx.re Platform Server (FXServer)
- `idms` → IDMS
- `portal` → Portal

💡 Se surgir um novo componente, use o `id` ou gere o slug do nome (minúsculas e traços). Para listar rapidamente:
```bash
curl -s https://status.cfx.re/api/v2/summary.json | jq -r '.components[] | [.id, (.name|ascii_downcase|gsub(\"[^a-z0-9]+\";\"-\"))] | @tsv'
```
Use o resultado em `CFX_SERVICE_FILTER` sem mudar código.

## ⚡ Exemplos rápidos
- Monitorar apenas FiveM, RedM e Keymaster por falhas graves:
  - `CFX_RULE_KIND=status`
  - `CFX_RULE_VALUE=major_outage,partial_outage`
  - `CFX_SERVICE_FILTER=fivem,redm,keymaster`
- Buscar padrão em JSON:
  - `CFX_RULE_KIND=regex`
  - `CFX_RULE_VALUE=error`
