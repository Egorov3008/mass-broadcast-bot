#!/usr/bin/env python3
"""
Создание репозитория на GitHub и пуш кода
"""

import subprocess
import os
import sys

# Получаем PAT из переменных окружения или файла
github_token = os.getenv('GITHUB_TOKEN')

if not github_token:
    # Пытаемся прочитать из файла
    try:
        with open('/root/.openclaw/secret/github.env', 'r') as f:
            for line in f:
                if line.startswith('GITHUB_TOKEN='):
                    github_token = line.split('=', 1)[1].strip()
                    break
    except:
        print("❌ Не удалось найти GITHUB_TOKEN")
        print("Создайте токен на https://github.com/settings/tokens")
        sys.exit(1)

print("🔑 GitHub PAT найден")
print(f"Токен: {github_token[:10]}...")

# Имя репозитория
repo_name = "mass-broadcast-bot"
owner = "Egorov3008"

# Создаем репозиторий через GitHub API
api_url = f"https://api.github.com/user/repos"

import json
import urllib.request

payload = {
    "name": repo_name,
    "private": False,
    "description": "Telegram Mass Broadcast Bot - рассылка сообщений пользователям с активными ключами",
    "homepage": "https://github.com/Egorov3008/mass-broadcast-bot",
    "auto_init": True
}

data = json.dumps(payload).encode('utf-8')

req = urllib.request.Request(api_url, data=data)
req.add_header('Authorization', f'token {github_token}')
req.add_header('Content-Type', 'application/json')

print(f"\n📦 Создание репозитория {repo_name}...")

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        print(f"✅ Репозиторий создан!")
        print(f"   Название: {result['name']}")
        print(f"   URL: {result['html_url']}")
        print(f"   Private: {result['private']}")
except urllib.error.HTTPError as e:
    if e.code == 422:
        print("⚠️ Репозиторий уже существует")
    else:
        print(f"❌ Ошибка создания: {e}")
        sys.exit(1)

# Добавляем remote и пушим
print(f"\n🔄 Добавление remote origin...")
subprocess.run(f"git remote add origin https://{github_token}@github.com/{owner}/{repo_name}.git", 
               shell=True, cwd="/root/.openclaw/workspace/mass-broadcast")

print(f"📤 Пуш в GitHub...")
subprocess.run(f"git branch -M main", shell=True, cwd="/root/.openclaw/workspace/mass-broadcast")
subprocess.run(f"git push -u origin main", shell=True, cwd="/root/.openclaw/workspace/mass-broadcast")

print("\n" + "="*70)
print("✅ ГОТОВО!")
print("="*70)
print(f"Репозиторий: https://github.com/{owner}/{repo_name}")
print("="*70)
