# Service monitor docker usage

1. Ajuste `.env` (já provisionado com valores default; use `.env.example` como referência se quiser resetar). A regra padrão do Steam usa `STEAM_RULE_KIND=status` e observa severidades `major,minor` na seção “Steam Services”; altere para `keyword`/`regex` se quiser outra lógica. Use `STEAM_SERVICE_FILTER` (lista separada por vírgulas) para monitorar apenas serviços específicos pelo `id` HTML (ex.: `store,community,webapi`); vazio monitora todos.
2. Build e start: `docker compose up --build` (rodar a partir desta pasta). O build usa `requirements.txt` na raiz.
3. Logs vão para stdout. Defaults carregam os módulos `steam` (HTML), `openai` (summary JSON), `claude` (summary JSON), `cfx` (summary JSON), `oci` (RSS), `gcp` (incidents JSON) e `aws` (current events JSON) a cada 60s.

Variáveis do módulo Steam (`STEAM_`):
- `STEAM_URL` (default `https://steamstat.us/`)
- `STEAM_RULE_KIND` (default `status`)
- `STEAM_RULE_VALUE` (default `major,minor`)
- `STEAM_SERVICE_FILTER` (ids de serviços; vazio = todos)
- `STEAM_ENABLED` (default `true`)

Variáveis do módulo OpenAI (`OPENAI_`):
- `OPENAI_URL` (default `https://status.openai.com/api/v2/summary.json`)
- `OPENAI_RULE_KIND` (default `status`)
- `OPENAI_RULE_VALUE` (default `degraded_performance,partial_outage,major_outage`)
- `OPENAI_SERVICE_FILTER` (slugs/ids de componentes; vazio = todos)
- `OPENAI_ENABLED` (default `true`)

Variáveis do módulo Claude (`CLAUDE_`):
- `CLAUDE_URL` (default `https://status.claude.com/api/v2/summary.json`)
- `CLAUDE_RULE_KIND` (default `status`)
- `CLAUDE_RULE_VALUE` (default `degraded_performance,partial_outage,major_outage`)
- `CLAUDE_SERVICE_FILTER` (slugs/ids de componentes; vazio = todos)
- `CLAUDE_ENABLED` (default `true`)

Variáveis do módulo Cfx (`CFX_`):
- `CFX_URL` (default `https://status.cfx.re/api/v2/summary.json`)
- `CFX_RULE_KIND` (default `status`)
- `CFX_RULE_VALUE` (default `degraded_performance,partial_outage,major_outage`)
- `CFX_SERVICE_FILTER` (slugs/ids de componentes; vazio = todos)
- `CFX_ENABLED` (default `true`)

Variáveis do módulo OCI (`OCI_`):
- `OCI_URL` (default `https://ocistatus.oraclecloud.com/api/v2/incident-summary.rss`)
- `OCI_RULE_KIND` (default `status`)
- `OCI_RULE_VALUE` (default `investigating,identified,monitoring`)
- `OCI_SERVICE_FILTER` (regiões/zonas; default `Brazil East (Sao Paulo),Brazil Southeast (Vinhedo)`)
- `OCI_ENABLED` (default `true`)

Variáveis do módulo GCP (`GCP_`):
- `GCP_URL` (default `https://status.cloud.google.com/incidents.json`)
- `GCP_RULE_KIND` (default `status`)
- `GCP_RULE_VALUE` (default `service_disruption,service_outage,service_information`)
- `GCP_SERVICE_FILTER` (ids de regiões; default `southamerica-east1,us-central1,us-east1`)
- `GCP_ENABLED` (default `true`)

Variáveis do módulo AWS (`AWS_`):
- `AWS_URL` (default `https://health.aws.amazon.com/public/currentevents`)
- `AWS_RULE_KIND` (default `status`)
- `AWS_RULE_VALUE` (default `operational_issue`)
- `AWS_SERVICE_FILTER` (ids de regiões; default `sa-east-1,us-east-1,us-east-2`)
- `AWS_ENABLED` (default `true`)

Notificações (Telegram):
- `TELEGRAM_ENABLED` (default `false`)
- `TELEGRAM_BOT_TOKEN` (obrigatório se habilitar)
- `TELEGRAM_CHAT_ID` (pode ser chat privado ou grupo; ignorado se `TELEGRAM_CHAT_IDS` for usado)
- `TELEGRAM_CHAT_IDS` (lista separada por vírgulas para enviar a múltiplos chats/grupos; use ids negativos para grupos)
- `TELEGRAM_API_URL` (default `https://api.telegram.org`)

Notificações (Webhook):
- `WEBHOOK_ENABLED` (default `false`)
- `WEBHOOK_URL` (endpoint alvo; obrigatório se habilitar)
- `WEBHOOK_TOKEN` (opcional; envia em header)
- `WEBHOOK_HEADER_NAME` (default `Authorization`)
- `NOTIFICATION_REPEAT_MINUTES` (minutos entre reenvio de alertas enquanto o incidente persiste; default `10`)

Variáveis de ativação:
- `STEAM_ENABLED`, `OPENAI_ENABLED`, `CLAUDE_ENABLED`, `CFX_ENABLED`, `OCI_ENABLED`, `GCP_ENABLED`, `AWS_ENABLED` (default `true`)

Key environment knobs:
- `SERVICE_MONITOR_MODULES`: comma list of module slugs to load (default `steam,openai,claude,cfx,oci,gcp,aws`).
- `SERVICE_MONITOR_DEFAULT_*`: fallback interval/timeout/user-agent used when module-specific envs are absent.
- `STEAM_RULE_KIND` / `STEAM_RULE_VALUE`: set `keyword` or `regex` matching against the steamstat.us HTML; a match yields an ALERT.

Para simular um alerta local, ajuste `STEAM_RULE_VALUE` para uma palavra que exista ou use uma regex que sempre case (ex.: `.*`). Reinicie `docker compose up` e acompanhe o log para ver um ALERT enquanto a aplicação continua rodando.
