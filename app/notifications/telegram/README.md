# 🔔 Telegram Notifier
![Channel](https://img.shields.io/badge/Channel-Telegram-2CA5E0)
![Format](https://img.shields.io/badge/Format-HTML-0A66C2)

🔗 Nav: [🏠 Home](../../../README.md) · [🎮 Steam](../../modules/steam/README.md) · [🔔 Notifications](../README.md) · [🐳 Docker](../../../DOCKER.md) · [📜 Spec](../../../openspec/changes/add-service-monitor-platform/specs/service-monitor/spec.md)

Envia cards HTML para chats ou grupos configurados quando um módulo retorna `ALERT` e quando um serviço é resolvido (`RESOLVED`). O texto padrão inclui módulo, status, motivo, horário do envio, resumo do payload e o tempo medido para a checagem.

## 🔧 Variáveis (`TELEGRAM_`)
- `TELEGRAM_ENABLED`: `true/false` para ativar o canal (default `false`).
- `TELEGRAM_BOT_TOKEN`: token do bot (obrigatório ao ativar); o request usa `/bot${TOKEN}/`.
- `TELEGRAM_CHAT_ID`: chat ou grupo (usado se `TELEGRAM_CHAT_IDS` estiver vazio).
- `TELEGRAM_CHAT_IDS`: lista separada por vírgulas para enviar a múltiplos chats/grupos (use ids negativos quando for grupo do Telegram).
- `TELEGRAM_API_URL`: endpoint da API (default `https://api.telegram.org`). Útil para proxies ou ambientes customizados.
- `TELEGRAM_TIMESTAMP_FORMAT`: format string used for the timestamp line (default `%Y-%m-%d %H:%M:%S %Z`).
- `TELEGRAM_TIMESTAMP_ZONE`: `UTC` (default) or `LOCAL`, determines whether the timestamp uses UTC or the host timezone.

## ✅ Validando o bot e destinatários
1. Verifique o token:  
   `curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe"` deve devolver `{"ok":true,...}` com o `username`.
2. Descubra o chat_id:
   - Envie uma mensagem para o bot (ou adicione-o a um grupo e envie `@<bot_username>`).
   - Rode `curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates"` e procure o campo `chat.id` no JSON.
   - Alternativamente, use bots como [@RawDataBot](https://t.me/RawDataBot) para expor o ID.
3. Para grupos, use o `chat.id` negativo retornado por `getUpdates` (ex.: `-4058878374`). Esse valor funciona tanto em `TELEGRAM_CHAT_ID` quanto em `TELEGRAM_CHAT_IDS`.

## 🧩 Template do card
O texto de alerta tem o formato:

```
🚨 *{MODULE_ID}* alerta
• Status: `{STATUS}`
• Motivo: {REASON}
• Quando: {UTC_TIMESTAMP}
• Detalhes: {SUMMARY} (opcional)
• Duração: `{DURATION_MS:.2f}ms`
```

O campo `Detalhes` resume o payload disponível (lista de serviços, objetos JSON, etc.) e é truncado para evitar mensagens muito longas. O `parse_mode=HTML` garante que o card seja exibido com destaque e separadores limpos.

O template HTML usado pelo bot está em `app/notifications/telegram/templates/telegram_alert.j2`; o módulo `steam` usa `telegram_steam.j2` para detalhar os serviços impactados e `telegram_resolved.j2` para a mensagem de resolução.

## 🚀 Como usar
1. Crie o bot com o [BotFather](https://t.me/BotFather) e recupere o token.
2. Ajuste `.env` com `TELEGRAM_ENABLED=true`, `TELEGRAM_BOT_TOKEN`, e o chat/grupo (via `TELEGRAM_CHAT_ID` ou `TELEGRAM_CHAT_IDS`).
3. Suba o monitor. Cada ALERT enviará o card a todos os chat_ids configurados.

## ℹ️ Notas
- Falhas de envio (timeout, chat bloqueado) são logadas como `notify_error` e não abortam o processo.
- Para novos canais, crie subdiretórios sob `app/notifications/<canal>` e registre-os em `NotificationManager`.
