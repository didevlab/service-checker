# 🔔 Webhook Notifier
![Channel](https://img.shields.io/badge/Channel-Webhook-6E56CF)
![Method](https://img.shields.io/badge/Method-POST-0A66C2)

🔗 Nav: [🏠 Home](../../../README.md) · [🎮 Steam](../../modules/steam/README.md) · [🔔 Notifications](../README.md) · [🐳 Docker](../../../DOCKER.md) · [📜 Spec](../../../openspec/changes/add-service-monitor-platform/specs/service-monitor/spec.md)

Dispara um POST para a `WEBHOOK_URL` sempre que um módulo entra em `ALERT` ou quando um serviço retorna a `OK` (evento `RESOLVED`). Você pode anexar um token no cabeçalho (`WEBHOOK_HEADER_NAME`) para autenticação.

## 🔧 Variáveis (`WEBHOOK_`)
- `WEBHOOK_ENABLED`: `true/false` para ativar o canal (default `false`).
- `WEBHOOK_URL`: endpoint receptor (obrigatório quando habilitado).
- `WEBHOOK_TOKEN`: token opcional que será enviado no header `WEBHOOK_HEADER_NAME`.
- `WEBHOOK_HEADER_NAME`: nome do header (default `Authorization`).

## 🚀 Payload enviado
```json
{
  "timestamp": "<iso8601>",
  "level": "<INFO|WARNING|ERROR>",
  "event": "<monitor_check|service_alert|service_resolved>",
  "module": "<module_id>",
  "status": "<ALERT|RESOLVED>",
  "message": "<result.message>",
  "reason": "<result.reason>",
  "payload": <result.payload>,
  "duration_ms": <result.duration_ms>
}
```

## ⚙️ Exemplo de uso
1. Habilite o canal: `WEBHOOK_ENABLED=true`.
2. Aponte `WEBHOOK_URL` para o seu endpoint e, se preciso, configure:
   - `WEBHOOK_TOKEN=Bearer abc123`
   - `WEBHOOK_HEADER_NAME=Authorization` (ou outro header que o receptor espera).
3. O monitor envia `POST` com o JSON acima a cada ALERT e loga falhas sem interromper o processo.
