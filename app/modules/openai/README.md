# 🤖 OpenAI Status Module
![Module](https://img.shields.io/badge/Module-OpenAI-1F6FEB)
![Source](https://img.shields.io/badge/Source-status.openai.com-0A66C2)

🔗 Nav: [🏠 Home](../../../README.md) · [🎮 Steam](../steam/README.md) · [🟣 Claude](../claude/README.md) · [🧭 Cfx](../cfx/README.md) · [☁️ OCI](../oci/README.md) · [🌐 GCP](../gcp/README.md) · [☁️ AWS](../aws/README.md) · [🔔 Notifications](../../notifications/README.md) · [🐳 Docker](../../../DOCKER.md) · [📜 Spec](../../../openspec/changes/add-service-monitor-platform/specs/service-monitor/spec.md)

Monitor da página https://status.openai.com/ usando o endpoint JSON `api/v2/summary.json`.

## 📚 Documentação principal
- README geral: [../../../README.md](../../../README.md)
- Docker: [../../../DOCKER.md](../../../DOCKER.md)

## 🧭 Visão geral
- Faz GET no summary JSON e avalia componentes por status.
- Estratégias suportadas: `status` (padrão), `keyword`, `regex`.
- O ciclo de alerta e resolução é por componente (cada `id`/`slug` gera ALERT/RESOLVED independente).
- Payload inclui os componentes avaliados (ou filtrados).

## 🔧 Variáveis de ambiente (`OPENAI_`)
- `URL` (default `https://status.openai.com/api/v2/summary.json`)
- `INTERVAL_SECONDS` (default 60)
- `TIMEOUT_SECONDS` (default 10)
- `USER_AGENT` (default herdado ou `service-monitor/openai`)
- `ENABLED`: `true/false` para ativar/desativar o módulo (default `true`)
- `RULE_KIND`: `status` (padrão), `keyword`, `regex`
- `RULE_VALUE`: para `status`, estados alvo (ex.: `degraded_performance,partial_outage,major_outage`); para `keyword`/`regex`, termo ou padrão
- `SERVICE_FILTER`: ids ou slugs de componentes a monitorar (ex.: `chat-completions`, `image-generation`, `login`); vazio = todos

## 🚦 Regra `status`
- Usa os estados do statuspage (`operational`, `degraded_performance`, `partial_outage`, `major_outage`, `under_maintenance`).
- Gera ALERT se algum componente filtrado tiver status presente em `RULE_VALUE`.

### 📇 Componentes conhecidos (slug → nome)
- `video-viewing` → Video viewing
- `embeddings` → Embeddings
- `video-generation` → Video generation
- `image-generation` → Image Generation
- `login` → Login
- `realtime` → Realtime
- `audio` → Audio
- `images` → Images
- `feed` → Feed
- `chat-completions` → Chat Completions
- `responses` → Responses
- `sora` → Sora
- `files` → Files
- `batch` → Batch
- `fine-tuning` → Fine-tuning
- `moderations` → Moderations
- `codex` → Codex
- `gpts` → GPTs
- `agent` → Agent
- `search` → Search
- `deep-research` → Deep Research
- `voice-mode` → Voice mode
- `chatgpt-atlas` → ChatGPT Atlas

💡 Se surgir um novo componente, use o `id` ou gere o slug do nome (minúsculas e traços). Para listar rapidamente:
```bash
curl -s https://status.openai.com/api/v2/summary.json | jq -r '.components[] | [.id, (.name|ascii_downcase|gsub(\"[^a-z0-9]+\";\"-\"))] | @tsv'
```
Use o resultado em `OPENAI_SERVICE_FILTER` sem mudar código.

## ⚡ Exemplos rápidos
- Monitorar apenas Chat Completions e Responses com foco em falhas graves:
  - `OPENAI_RULE_KIND=status`
  - `OPENAI_RULE_VALUE=major_outage,partial_outage`
  - `OPENAI_SERVICE_FILTER=chat-completions,responses`
- Buscar padrão em JSON:
  - `OPENAI_RULE_KIND=regex`
  - `OPENAI_RULE_VALUE=error`
