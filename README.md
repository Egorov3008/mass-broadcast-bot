# Mass Broadcast Bot

Telegram bot for mass message broadcasting to users with active subscription keys.

## 🚀 Features

- Mass messaging via Pyrogram API
- User list from PostgreSQL database via SSH tunnel
- Active key filtering (only users with valid subscriptions)
- Flood wait handling
- Detailed statistics after broadcast
- Session persistence

## 📦 Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🔐 Configuration

1. **Get Telegram API credentials from** [my.telegram.org](https://my.telegram.org)

2. **Create `.env` file:**
```bash
cp .env.example .env
```

3. **Edit `.env`:**
```bash
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=+79322490462
```

## 🚀 Usage

### Authorize first time:

```bash
python mass_broadcast.py --message "Test" --delay 1
```

Enter SMS code from Telegram.

### Broadcast messages:

```bash
python mass_broadcast.py --message "Your message here" --delay 5
```

### Parameters:

- `--message` (required): Message text to broadcast
- `--delay`: Delay between messages in seconds (default: 5)
- `--api-id`: Telegram API ID
- `--api-hash`: Telegram API Hash
- `--phone`: Phone number for authorization
- `--users-file`: Path to users file (default: users_with_active_keys.txt)

## 📊 Database

Users with active keys are fetched from PostgreSQL database:

```sql
SELECT DISTINCT k.tg_id FROM keys k 
WHERE k.expiry_time > EXTRACT(EPOCH FROM CURRENT_TIMESTAMP) 
ORDER BY k.tg_id;
```

### Get users from database:

```bash
python get_users_from_db.py
```

This creates `users_with_active_keys.txt` with active users.

## ⚙️ Systemd Service (optional)

Create `/etc/systemd/system/mass-broadcast.service`:

```ini
[Unit]
Description=Mass Broadcast Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/mass-broadcast
ExecStart=/root/.openclaw/workspace/mass-broadcast/venv/bin/python mass_broadcast.py --message "Broadcast" --delay 5
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable mass-broadcast
sudo systemctl start mass-broadcast
```

## 📝 Statistics

After broadcast completes:

```
📊 СТАТИСТИКА РАССЫЛКИ
============================================================
Всего получателей: 125
✅ Отправлено: 120
🚫 Заблокировано: 3
❌ Ошибки: 2
Успешно: 96.0%
============================================================
```

## 🛡️ Security

- **DO NOT commit `.env` files** - contains API credentials
- **DO NOT commit `users_with_active_keys.txt`** - contains user IDs
- Store API credentials in secure location
- Use SSH tunnel for database access
- Rate limiting with flood wait handling

## 📁 File Structure

```
mass-broadcast/
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── mass_broadcast.py         # Main broadcast script
├── get_users_from_db.py      # Generate user list
└── users_with_active_keys.txt # (generated, not committed)
```

## 📄 License

MIT License

## 👤 Author

Created for personal use. Feel free to fork and modify.
