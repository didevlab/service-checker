# 🔔 Webhook Notifier
![Channel](https://img.shields.io/badge/Channel-Webhook-6E56CF)
![Method](https://img.shields.io/badge/Method-POST-0A66C2)

🔗 Nav: [🏠 Home](../../../README.md) · [🎮 Steam](../../modules/steam/README.md) · [🔔 Notifications](../README.md) · [🐳 Docker](../../../DOCKER.md)

Sends a POST to `WEBHOOK_URL` whenever a module enters `ALERT` or when a service returns to `OK` (`RESOLVED` event). You can attach a token in the header (`WEBHOOK_HEADER_NAME`) for authentication.

## 🔧 Variables (`WEBHOOK_`)
- `WEBHOOK_ENABLED`: `true/false` to enable the channel (default `false`).
- `WEBHOOK_URL`: receiver endpoint (required when enabled).
- `WEBHOOK_TOKEN`: optional token sent in the `WEBHOOK_HEADER_NAME` header.
- `WEBHOOK_HEADER_NAME`: header name (default `Authorization`).

## 🚀 Payload sent
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

## ⚙️ Usage example
1. Enable the channel: `WEBHOOK_ENABLED=true`.
2. Point `WEBHOOK_URL` to your endpoint and, if needed, set:
   - `WEBHOOK_TOKEN=Bearer abc123`
   - `WEBHOOK_HEADER_NAME=Authorization` (or another header expected by the receiver).
3. The monitor sends the JSON above on every ALERT and logs failures without stopping the process.
