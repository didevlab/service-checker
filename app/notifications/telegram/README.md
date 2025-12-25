# 🔔 Telegram Notifier
![Channel](https://img.shields.io/badge/Channel-Telegram-2CA5E0)
![Format](https://img.shields.io/badge/Format-HTML-0A66C2)

🔗 Nav: [🏠 Home](../../../README.md) · [🎮 Steam](../../modules/steam/README.md) · [🔔 Notifications](../README.md) · [🐳 Docker](../../../DOCKER.md)

Sends HTML cards to configured chats or groups when a module returns `ALERT` and when a service is resolved (`RESOLVED`). The default text includes module, status, reason, send time, payload summary, and measured check duration.

## 🔧 Variables (`TELEGRAM_`)
- `TELEGRAM_ENABLED`: `true/false` to enable the channel (default `false`).
- `TELEGRAM_BOT_TOKEN`: bot token (required when enabled); the request uses `/bot${TOKEN}/`.
- `TELEGRAM_CHAT_ID`: chat or group (used if `TELEGRAM_CHAT_IDS` is empty).
- `TELEGRAM_CHAT_IDS`: comma-separated list to send to multiple chats/groups (use negative IDs for Telegram groups).
- `TELEGRAM_API_URL`: API endpoint (default `https://api.telegram.org`). Useful for proxies or custom environments.
- `TELEGRAM_TIMESTAMP_FORMAT`: format string used for the timestamp line (default `%Y-%m-%d %H:%M:%S %Z`).
- `TELEGRAM_TIMESTAMP_ZONE`: `UTC` (default) or `LOCAL`, determines whether the timestamp uses UTC or the host timezone.

## ✅ Validating the bot and recipients
1. Check the token:  
   `curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe"` should return `{"ok":true,...}` with the `username`.
2. Find the chat_id:
   - Send a message to the bot (or add it to a group and mention `@<bot_username>`).
   - Run `curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates"` and look for `chat.id` in the JSON.
   - Alternatively, use bots like [@RawDataBot](https://t.me/RawDataBot) to expose the ID.
3. For groups, use the negative `chat.id` returned by `getUpdates` (e.g., `-4058878374`). This works for both `TELEGRAM_CHAT_ID` and `TELEGRAM_CHAT_IDS`.

## 🧩 Card template
The alert text has the format:

```
🚨 *{MODULE_ID}* alert
• Status: `{STATUS}`
• Reason: {REASON}
• When: {UTC_TIMESTAMP}
• Details: {SUMMARY} (optional)
• Duration: `{DURATION_MS:.2f}ms`
```

The `Details` field summarizes the available payload (service list, JSON objects, etc.) and is truncated to avoid overly long messages. `parse_mode=HTML` ensures the card displays with emphasis and clean separators.

The HTML template used by the bot lives at `app/notifications/telegram/templates/telegram_alert.j2`; the `steam` module uses `telegram_steam.j2` to detail impacted services and `telegram_resolved.j2` for the resolution message.

## 🚀 How to use
1. Create the bot with [BotFather](https://t.me/BotFather) and grab the token.
2. Update `.env` with `TELEGRAM_ENABLED=true`, `TELEGRAM_BOT_TOKEN`, and the chat/group via `TELEGRAM_CHAT_ID` or `TELEGRAM_CHAT_IDS`.
3. Start the monitor. Each ALERT will send the card to all configured chat_ids.

## ℹ️ Notes
- Send failures (timeouts, blocked chat) are logged as `notify_error` and do not abort the process.
- For new channels, create subdirectories under `app/notifications/<channel>` and register them in `NotificationManager`.
