# 📝 MASS BROADCAST BOT - QUICK START

## 🎯 What You Need

1. **API Credentials** (already configured):
   - API ID: `36442196`
   - API Hash: `2c764877adb42800cb5f7af9252f2990`
   - Phone: `+79322490462`

2. **Users File** (generated from database):
   - Run: `python get_users_from_db.py`

3. **Authorization** (one-time setup)

---

## 🚀 Quick Start (5 Steps)

### **Step 1: Install Dependencies**

```bash
cd /root/.openclaw/workspace/mass-broadcast
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Step 2: Authorize Bot**

```bash
python scripts/authorizer.py
```

**Enter SMS code** when prompted (will be sent to `+79322490462`)

### **Step 3: Generate Users List**

```bash
python get_users_from_db.py
```

This creates `users_with_active_keys.txt` with active subscribers.

### **Step 4: Test Broadcast**

```bash
python mass_broadcast.py --message "🔥 Test message from Mass Broadcast Bot!" --delay 1
```

### **Step 5: Full Broadcast**

```bash
python mass_broadcast.py --message "📢 Your important message here" --delay 5
```

---

## 📊 Example Output

```
======================================================================
📢 STARTING MASS BROADCAST
======================================================================
👥 Recipients: 125
📝 Message: 📢 Your important message here...
⏱️ Delay: 5s
======================================================================

[1/125] Sending to 40885425...
[2/125] Sending to 52829147...
...
[125/125] Sending to 8579660082...

======================================================================
📊 BROADCAST STATISTICS
======================================================================
Total recipients: 125
✅ Success: 122
❌ Errors: 3
📈 Success rate: 97.6%
======================================================================

🔌 Disconnected from Telegram
```

---

## 🛠️ Command Options

```bash
python mass_broadcast.py --help
```

Available options:
- `--message, -m`: Message text (required)
- `--delay, -d`: Delay between messages (default: 5)
- `--api-id`: Telegram API ID (optional, uses config)
- `--api-hash`: Telegram API Hash (optional, uses config)
- `--phone`: Phone number (optional, uses config)
- `--users-file`: Path to users file (optional, default: users_with_active_keys.txt)

---

## 🔒 Security Notes

- ✅ `.env` files are **NOT** committed to git
- ✅ `users_with_active_keys.txt` is **NOT** committed (generated locally)
- ✅ Session data is stored in `sessions/` directory
- ✅ All credentials stored locally only

---

## 📁 Project Structure

```
mass-broadcast/
├── main.py                      # Main entry point (new)
├── mass_broadcast.py            # Original version (backward compatible)
├── get_users_from_db.py         # Generate users from database
├── requirements.txt             # Python dependencies
├── README.md                    # Full documentation
├── SETUP.md                     # Quick start guide
├── .gitignore                   # Git ignore rules
├── .env.example                 # Environment template
│
├── scripts/                     # New modular structure
│   ├── __init__.py
│   ├── config.py                # Configuration
│   ├── tg_client.py             # Pyrogram client builder
│   ├── authorizer.py            # Quick authorization
│   └── auth_and_check.py        # Authorization checker
│
├── sessions/                    # Pyrogram session storage
└── venv/                        # Virtual environment
```

---

## 🐛 Troubleshooting

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Session not found"
Run authorizer first:
```bash
python scripts/authorizer.py
```

### "FloodWait error"
Increase delay:
```bash
python mass_broadcast.py --message "..." --delay 10
```

---

## 🎯 Next Steps

1. ✅ **Authorize**: `python scripts/authorizer.py`
2. ✅ **Generate users**: `python get_users_from_db.py`
3. ✅ **Test**: `python mass_broadcast.py --message "Test" --delay 1`
4. ✅ **Broadcast**: `python mass_broadcast.py --message "Your message" --delay 5`

---

**Need help?** Check `README.md` or `SETUP.md` for detailed documentation.
