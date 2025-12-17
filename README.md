# Telegram Group Management Bot

Bot Telegram untuk menguruskan group dengan features seperti welcome message, moderasi link, sistem amaran, dan mesej berjadual.

## Features

✅ **Welcome Message** - Hantar mesej selamat datang kepada ahli baru
✅ **Link Moderation** - Auto-delete link yang tidak dibenarkan
✅ **Warning System** - Sistem amaran 3 kali sebelum kick
✅ **Auto Kick** - Keluarkan ahli yang melanggar peraturan
✅ **Scheduled Messages** - Hantar mesej mengikut jadual
✅ **Motivational Quotes** - Kongsi quote motivasi

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Bot Token

Dapatkan Bot Token dari [@BotFather](https://t.me/BotFather) di Telegram:

1. Start chat dengan @BotFather
2. Gunakan command `/newbot`
3. Ikuti arahan untuk create bot baru
4. Copy Bot Token yang diberikan

Edit file `.env` dan masukkan Bot Token:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 3. Setup Bot Permissions

Pastikan bot mempunyai permissions berikut dalam group:

- Delete messages
- Ban users
- Read messages

Untuk set permissions:
1. Tambah bot ke group anda
2. Promote bot sebagai admin
3. Enable permissions yang diperlukan

### 4. Run Bot

```bash
python bot.py
```

## Bot Commands

- `/start` - Mulakan bot dan lihat info
- `/help` - Paparkan semua command
- `/quote` - Dapatkan quote motivasi rawak
- `/stats` - Lihat statistik amaran anda

## Database Schema

Bot menggunakan Supabase dengan tables berikut:

### user_warnings
Simpan rekod amaran untuk setiap user

### scheduled_messages
Simpan mesej berjadual

### motivational_quotes
Simpan koleksi quote motivasi

### group_settings
Simpan settings untuk setiap group

## Cara Guna

### Scheduled Messages

Untuk add mesej berjadual, tambah data dalam table `scheduled_messages`:

```sql
INSERT INTO scheduled_messages (chat_id, message_text, schedule_time, schedule_days, is_active)
VALUES (-1001234567890, 'Selamat Pagi!', '09:00', ARRAY['monday', 'friday'], true);
```

### Add Custom Quotes

Untuk tambah quote baru:

```sql
INSERT INTO motivational_quotes (quote_text, author, is_active)
VALUES ('Your quote here', 'Author Name', true);
```

### Customize Welcome Message

Update dalam table `group_settings`:

```sql
UPDATE group_settings
SET welcome_message = 'Custom welcome message anda'
WHERE chat_id = -1001234567890;
```

## Troubleshooting

**Bot tidak delete messages?**
- Pastikan bot adalah admin dengan permission "Delete messages"

**Bot tidak kick users?**
- Pastikan bot adalah admin dengan permission "Ban users"

**Scheduled messages tidak send?**
- Check format time menggunakan 24-hour format (HH:MM)
- Pastikan `is_active` adalah true

## Support

Untuk issues atau questions, sila contact developer.
