# Mass Broadcast Bot

Telegram bot for mass message broadcasting to users with active subscription keys.

## 🚀 Features

- ✅ Mass messaging via Pyrogram API
- ✅ User list from PostgreSQL database via SSH tunnel
- ✅ Active key filtering (only users with valid subscriptions)
- ✅ Flood wait handling
- ✅ Detailed statistics after broadcast
- ✅ Modular structure with separate scripts
- ✅ Quick authorization tool

## 📚 Quick Start

**📖 See [QUICK_START.md](QUICK_START.md) for step-by-step guide**

**📖 See [SETUP.md](SETUP.md) for detailed installation**

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

2. **Copy environment template:**
```bash
cp .env.example .env
```

3. **Edit `.env`:**
```bash
TELEGRAM_API_ID=36442196
TELEGRAM_API_HASH=2c764877adb42800cb5f7af9252f2990
TELEGRAM_PHONE=+79322490462
```

## 🚀 Usage

### **1. Authorize Bot (First Time)**

```bash
python scripts/authorizer.py
```

Enter SMS code from Telegram.

### **2. Generate User List**

```bash
python get_users_from_db.py
```

This fetches users with active keys from PostgreSQL and creates `users_with_active_keys.txt`.

### **3. Test Broadcast**

```bash
python mass_broadcast.py --message "🔥 Test message!" --delay 1
```

### **4. Full Broadcast**

```bash
python mass_broadcast.py --message "📢 Your important message" --delay 5
```

### **Parameters**

- `--message, -m`: Message text to broadcast (required)
- `--delay, -d`: Delay between messages in seconds (default: 5)
- `--api-id`: Telegram API ID (optional)
- `--api-hash`: Telegram API Hash (optional)
- `--phone`: Phone number for authorization (optional)
- `--users-file`: Path to users file (default: users_with_active_keys.txt)

## 📊 Database

Users with active keys are fetched from PostgreSQL database:

```sql
SELECT DISTINCT k.tg_id FROM keys k 
WHERE k.expiry_time > EXTRACT(EPOCH FROM CURRENT_TIMESTAMP) 
ORDER BY k.tg_id;
```

## ⚙️ Project Structure

```
mass-broadcast/
├── main.py                      # Main entry point
├── mass_broadcast.py            # Original broadcast script
├── get_users_from_db.py         # Generate user list from DB
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── QUICK_START.md               # Quick start guide
├── SETUP.md                     # Detailed setup
│
├── scripts/                     # Modular structure
│   ├── __init__.py
│   ├── config.py                # Configuration
│   ├── tg_client.py             # Pyrogram client builder
│   ├── authorizer.py            # Quick authorization
│   └── auth_and_check.py        # Authorization checker
│
├── sessions/                    # Pyrogram session storage
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
└── venv/                        # Virtual environment
```

## 📝 Statistics

After broadcast completes:

```
======================================================================
📊 BROADCAST STATISTICS
======================================================================
Total recipients: 125
✅ Success: 122
❌ Errors: 3
📈 Success rate: 97.6%
======================================================================
```

## 🛡️ Security

- ✅ **DO NOT commit `.env` files** - contains API credentials
- ✅ **DO NOT commit `users_with_active_keys.txt`** - contains user IDs
- ✅ Store API credentials in secure location
- ✅ Use SSH tunnel for database access
- ✅ Rate limiting with flood wait handling
- ✅ Session data stored locally

## 🐛 Troubleshooting

### "Module not found"
```bash
source venv/bin/activate
pip install pyrogram
```

### "FloodWait" errors
Script automatically handles flood waits. Increase `--delay`:
```bash
python mass_broadcast.py --message "..." --delay 10
```

### "Session not found"
Run authorizer first:
```bash
python scripts/authorizer.py
```

## 📄 License

MIT License

## 👤 Author

Created for personal use. Feel free to fork and modify.

## 🔗 Links

- **GitHub Repository**: https://github.com/Egorov3008/mass-broadcast-bot
- **Pyrogram Docs**: https://docs.pyrogram.ai/
- **Telegram API**: https://core.telegram.org/api/obtaining_api_id
