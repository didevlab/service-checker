# 🎮 Steam Module
![Module](https://img.shields.io/badge/Module-Steam-1F6FEB)
![Source](https://img.shields.io/badge/Source-steamstat.us-0A66C2)

🔗 Nav: [🏠 Home](../../../README.md) · [🤖 OpenAI](../openai/README.md) · [🟣 Claude](../claude/README.md) · [🧭 Cfx](../cfx/README.md) · [☁️ OCI](../oci/README.md) · [🌐 GCP](../gcp/README.md) · [☁️ AWS](../aws/README.md) · [🔔 Notifications](../../notifications/README.md) · [🐳 Docker](../../../DOCKER.md) · [📜 Spec](../../../openspec/changes/add-service-monitor-platform/specs/service-monitor/spec.md)

Monitor do https://steamstat.us/ com regras configuráveis por ambiente e filtro de serviços.

## 📚 Documentação principal
- README geral: [../../../README.md](../../../README.md)
- Docker: [../../../DOCKER.md](../../../DOCKER.md)

## 🧭 Visão geral
- Puxa o HTML da página e aplica a regra definida em env.
- Suporta três estratégias: `status`, `keyword`, `regex`.
- Resultado inclui payload com os serviços avaliados para auditoria.
- O ciclo de alerta e resolução é por serviço (cada `id` da Steam Services recebe ALERT/RESOLVED independente).

## 🔧 Variáveis de ambiente (`STEAM_`)
- `URL` (default `https://steamstat.us/`)
- `INTERVAL_SECONDS` (default 60)
- `TIMEOUT_SECONDS` (default 10)
 - `USER_AGENT` (default herdado ou `service-monitor/steam`)
- `ENABLED`: `true/false` para ativar/desativar o módulo (default `true`)
- `RULE_KIND`: `status` (padrão), `keyword`, `regex`
- `RULE_VALUE`: para `status`, severidades alvo (ex.: `major,minor`); para `keyword`/`regex`, termo ou padrão
 - `SERVICE_FILTER`: ids de serviços a monitorar (ex.: `store,community,webapi`); vazio = todos

## 🚦 Regra `status`
- Faz parse da seção “Steam Services” e coleta id, nome, severidade (`good`, `minor`, `major`) e texto.
- Gera ALERT se qualquer serviço filtrado tiver severidade listada em `RULE_VALUE`.
- Payload retorna a lista de serviços avaliados (ou apenas os filtrados).

### 📇 IDs de serviço conhecidos
`online`, `ingame`, `store`, `community`, `webapi`, `cms`, `cs2`, `cs_sessions`, `cs_community`, `cs_mm_scheduler`, `deadlock`, `dota2`, `tf2`, `bot`, `database`, `pageviews` (e demais que aparecem na página).

💡 Se surgir um novo serviço não listado aqui, basta pegar o `id` mostrado no HTML da página (atributo `id` do elemento `<span class="status ...">`). Exemplo rápido:
```bash
curl -s https://steamstat.us/ | rg -o 'status [^"]+" id="([^"]+)"' | sed 's/.*id=\"//;s/\"$//'
```
Use o valor obtido em `STEAM_SERVICE_FILTER` sem precisar alterar código.

## ⚡ Exemplos rápidos
- Monitorar só Store/Community/Web API por falha grave:
  - `STEAM_RULE_KIND=status`
  - `STEAM_RULE_VALUE=major`
  - `STEAM_SERVICE_FILTER=store,community,webapi`
- Termo específico:
  - `STEAM_RULE_KIND=keyword`
  - `STEAM_RULE_VALUE=offline`
