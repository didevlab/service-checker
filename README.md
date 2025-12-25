# ⚙️ Service Monitor
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![Notifications](https://img.shields.io/badge/Notifications-Telegram%20%7C%20Webhook-26A5E4)

🔗 Nav: [🎮 Steam](app/modules/steam/README.md) · [🤖 OpenAI](app/modules/openai/README.md) · [🟣 Claude](app/modules/claude/README.md) · [🧭 Cfx](app/modules/cfx/README.md) · [☁️ OCI](app/modules/oci/README.md) · [🌐 GCP](app/modules/gcp/README.md) · [☁️ AWS](app/modules/aws/README.md) · [🔔 Notifications](app/notifications/README.md) · [🐳 Docker](DOCKER.md)

Monitor Python modular que checa páginas de status de terceiros (Steam, OpenAI, Claude, Cfx, OCI, GCP e AWS) e dispara notificações configuráveis quando qualquer módulo gera ALERT.

## 📘 Estrutura
- `app/`: core, módulos (`steam`, `openai`, `claude`, `cfx`, `oci`, `gcp`, `aws`) e notificadores.
- `docker-compose.yml`, `Dockerfile` e `.env(.example)` ficam na raiz para facilitar implantação local e no container.

## 📦 Módulos
- 🎮 **Steam**: rastreia https://steamstat.us/, aplica regras `status`/`keyword`/`regex` sobre a seção “Steam Services” e publica quais serviços estão fora do ar. [app/modules/steam/README.md](app/modules/steam/README.md)
- 🤖 **OpenAI Status**: consome `https://status.openai.com/api/v2/summary.json`, filtra componentes/ids e gera ALERT para incidentes degradados ou apagões. [app/modules/openai/README.md](app/modules/openai/README.md)
- 🟣 **Claude Status**: monitora `https://status.claude.com/api/v2/summary.json`, suporta filtragem por componentes e filtros `keyword/regex`. [app/modules/claude/README.md](app/modules/claude/README.md)
- 🧭 **Cfx Status**: consome `https://status.cfx.re/api/v2/summary.json` para detectar degraded/partial/major outages por componente. [app/modules/cfx/README.md](app/modules/cfx/README.md)
- ☁️ **OCI Status (LAD)**: usa o RSS `https://ocistatus.oraclecloud.com/api/v2/incident-summary.rss`, monitorando LAD (default Brazil East/Brazil Southeast). [app/modules/oci/README.md](app/modules/oci/README.md)
- 🌐 **GCP Status (Americas)**: consulta `https://status.cloud.google.com/incidents.json`, foca em regiões `southamerica-east1`, `us-central1`, `us-east1`. [app/modules/gcp/README.md](app/modules/gcp/README.md)
- ☁️ **AWS Status**: busca `https://health.aws.amazon.com/public/currentevents`, filtra eventos ativos e regiões `sa-east-1`, `us-east-1`, `us-east-2`. [app/modules/aws/README.md](app/modules/aws/README.md)

## 🔔 Notificações
O `NotificationManager` central dispara os canais habilitados sempre que um módulo entra em `ALERT` ou quando um serviço volta a `OK`. A implementação atual oferece:
- **Telegram**: envia cards HTML (`Service-Checker — Alert/Resolved`) para um ou mais chats/grupos. Configure `TELEGRAM_ENABLED=true`, `TELEGRAM_BOT_TOKEN`, e informe `TELEGRAM_CHAT_ID` ou `TELEGRAM_CHAT_IDS` (use ids negativos para grupos). Ajuste `TELEGRAM_TIMESTAMP_FORMAT` (default `%Y-%m-%d %H:%M:%S %Z`) e `TELEGRAM_TIMESTAMP_ZONE` (`UTC` ou `LOCAL`) para controlar o formato e a zona do timestamp. Consulte [app/notifications/telegram/README.md](app/notifications/telegram/README.md) para saber como validar o token via `getMe`, descobrir o chat_id (ex.: envie uma mensagem ao bot e use `https://api.telegram.org/bot$TOKEN/getUpdates`), e como os templates são estruturados.
- **Webhook**: dispara um POST JSON para `WEBHOOK_URL` com eventos `ALERT` ou `RESOLVED` e opcional `WEBHOOK_TOKEN`/`WEBHOOK_HEADER_NAME` para autenticação. Veja o [README do webhook](app/notifications/webhook/README.md) para payload e exemplos.

## 🚀 Uso rápido
1. Ajuste `.env` (ou `.env.example`) com suas chaves e filtros.
2. Execute `docker compose up --build` no diretório raiz.
3. Verifique logs com `docker compose logs --tail 20` ou via `docker logs <container>`.

## 🧰 Configuração
- `SERVICE_MONITOR_MODULES` controla os módulos carregados (default `steam,openai,claude,cfx,oci,gcp,aws`).
- Cada módulo respeita `<PREFIX>_ENABLED` (default `true`), `<PREFIX>_RULE_*`, `<PREFIX>_SERVICE_FILTER`, etc.
- Ative notificações por `TELEGRAM_ENABLED=true` e/ou `WEBHOOK_ENABLED=true`. Caso uma notificação falhe, o monitor continua rodando; erros são logados.
- Controle o intervalo de repetição de alertas com `NOTIFICATION_REPEAT_MINUTES` (minutos; default `10`).
- Para módulos que retornam lista de serviços (Steam, OpenAI, etc.), o ciclo é **por serviço**: alertas, repetição e resolução são rastreados individualmente.

## 🧪 CI & Publicação
- O workflow de release (`.github/workflows/release.yml`) executa semantic-release em `main` com Conventional Commits, gera tags `vX.Y.Z`, publica GitHub Releases e atualiza `CHANGELOG.md`.
- O workflow de publicação (`.github/workflows/publish.yml`) dispara em tags `v*` e publica a imagem no GitHub Container Registry (`ghcr.io/${{ github.repository_owner }}/service-monitor`) com tags `latest` e `vX.Y.Z`.
- Ambos usam o `GITHUB_TOKEN` padrão; garanta permissões de `contents: write` e `packages: write` para criar releases e publicar imagens.

## 🔗 Documentação rápida
- Módulos: [Steam](app/modules/steam/README.md), [OpenAI](app/modules/openai/README.md), [Claude](app/modules/claude/README.md), [Cfx](app/modules/cfx/README.md), [OCI](app/modules/oci/README.md), [GCP](app/modules/gcp/README.md), [AWS](app/modules/aws/README.md)
- Notificações: [notifier overview](app/notifications/README.md) · [Telegram](app/notifications/telegram/README.md) · [Webhook](app/notifications/webhook/README.md)
- Infra: [DOCKER.md](DOCKER.md), [docker-compose.yml](docker-compose.yml)
