# 🔔 Notifications
![Notifications](https://img.shields.io/badge/Notifications-Telegram%20%7C%20Webhook-26A5E4)
![Flow](https://img.shields.io/badge/Lifecycle-Alert%20%26%20Resolved-2EA44F)

🔗 Nav: [🏠 Home](../../README.md) · [🎮 Steam](../modules/steam/README.md) · [🐳 Docker](../../DOCKER.md) · [📜 Spec](../../openspec/changes/add-service-monitor-platform/specs/service-monitor/spec.md)

O `NotificationManager` (em `app/core/notifications.py`) recebe os resultados dos módulos e dispara cada canal habilitado sempre que um monitor retorna `ALERT` ou quando um serviço volta a `OK` (mensagem de resolução).

## 🧭 Visão geral
- Cada módulo é responsável por chamar o handler do `NotificationManager`; o core não precisa conhecer detalhes de cada destino.
- Para módulos que retornam lista de serviços (Steam/OpenAI/etc.), o ciclo é por serviço (alerta, repetição e resolução independentes).
- Canais disponíveis: Telegram (`app/notifications/telegram`) e Webhook (`app/notifications/webhook`). Novos destinos podem ser adicionados seguindo o mesmo contrato.
- Falhas de notificação são logadas com nível `ERROR`, mas não abortam o monitor principal.

## 🔧 Variáveis
- `TELEGRAM_*`: habilita o bot, informa o token, permite múltiplos chat_ids (`TELEGRAM_CHAT_IDS`) e opcionalmente altera a URL da API (`TELEGRAM_API_URL`). Use ids negativos para grupos.
- `NOTIFICATION_REPEAT_MINUTES`: tempo mínimo (minutos) para repetir alertas do mesmo serviço enquanto o incidente persiste (default `10`).
- `WEBHOOK_*`: habilita o envio e envia um POST JSON para `WEBHOOK_URL`, com token opcional em `WEBHOOK_HEADER_NAME`.

## 📚 Leituras recomendadas
- [Telegram](telegram/README.md): explica como validar o token (`getMe`), descobrir `chat_id` ou grupo via `getUpdates`, e mostra o template do card Markdown.
- [Webhook](webhook/README.md): descreve payload, headers e exemplos de uso.
