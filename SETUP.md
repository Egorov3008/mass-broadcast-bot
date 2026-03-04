# 🚀 SETUP INSTRUCTIONS - Mass Broadcast Bot

## ⚡ Quick Start

### 1. Clone repository

```bash
git clone https://github.com/Egorov3008/mass-broadcast-bot.git
cd mass-broadcast-bot
```

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create environment file

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```bash
TELEGRAM_API_ID=36442196
TELEGRAM_API_HASH=2c764877adb42800cb5f7af9252f2990
TELEGRAM_PHONE=+79322490462
```

### 4. Generate user list (one-time)

```bash
python get_users_from_db.py
```

This will fetch users with active keys from your PostgreSQL database and create `users_with_active_keys.txt`.

### 5. Test broadcast

```bash
python mass_broadcast.py --message "🔥 Test message from Mass Broadcast Bot!" --delay 5
```

### 6. Run full broadcast

```bash
python mass_broadcast.py --message "📢 Important update for all users! Check your subscription status." --delay 3
```

## 📊 Expected Output

```
📢 НАЧАЛО МАССОВОЙ РАССЫЛКИ
============================================================
👥 Получателей: 125
📝 Сообщение: 📢 Important update for all users! Check...
⏱️ Задержка: 3 сек
============================================================
[1/125] Отправка (ID: 40885425)
[2/125] Отправка (ID: 52829147)
...
[125/125] Отправка (ID: 8579660082)

📊 СТАТИСТИКА РАССЫЛКИ
============================================================
Всего получателей: 125
✅ Отправлено: 122
🚫 Заблокировано: 2
❌ Ошибки: 1
Успешно: 97.6%
============================================================
```

## 🔒 Security

- ✅ `.env` file is NOT committed to git
- ✅ `users_with_active_keys.txt` is NOT committed (generated locally)
- ✅ SSH tunnel for database access
- ✅ All user IDs anonymized

## 🐛 Troubleshooting

### "No module named 'pyrogram'"

```bash
source venv/bin/activate
pip install pyrogram
```

### "Permission denied" for SSH

Check SSH credentials in `get_users_from_db.py`:
```python
SSH_PASSWORD = "tMtB1Ri9JRphMct"
```

### "FloodWait" errors

Script automatically handles flood waits. Increase `--delay` parameter:
```bash
python mass_broadcast.py --message "..." --delay 10
```

### User blocked the bot

Statistics will show "🚫 Заблокировано: X" - these users won't receive future messages.

## 📝 Next Steps

1. ✅ Create `.env` file with your credentials
2. ✅ Generate user list: `python get_users_from_db.py`
3. ✅ Test with: `python mass_broadcast.py --message "Test" --delay 1`
4. ✅ Run full broadcast: `python mass_broadcast.py --message "Your message" --delay 5`

## 🎯 Tips

- Use `--delay 1-2` for small user lists (< 50)
- Use `--delay 5-10` for large lists (> 100)
- Monitor logs for "FloodWait" warnings
- Check statistics after each broadcast
- Never use delay < 1 second (risk of ban)

---

**Need help?** Check the README.md or GitHub issues.
