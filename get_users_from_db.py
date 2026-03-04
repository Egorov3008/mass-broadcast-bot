#!/usr/bin/env python3
"""
Загрузка пользователей с активными ключами из базы данных
"""

import subprocess
from pathlib import Path

# Настройки SSH
SSH_CMD = "sshpass -p 'tMtB1Ri9JRphMct' ssh -o StrictHostKeyChecking=no -p 65322 egorov@176.32.39.15"

# База данных
DB_NAME = "bot_db"
DB_USER = "egorov"


def run_ssh_command(command):
    """Выполняет команду через SSH"""
    full_cmd = f"{SSH_CMD} {command}"
    
    try:
        result = subprocess.run(
            full_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), -1


def main():
    """Основная функция"""
    print("=" * 70)
    print("🔌 ПОДКЛЮЧЕНИЕ К POSTGRESQL ЧЕРЕЗ SSH")
    print("=" * 70)
    
    # Получаем только активные ключи
    print("\n📊 Получение пользователей с активными ключами...")
    
    cmd = f"psql -d {DB_NAME} -U {DB_USER} -t -A -c \"SELECT DISTINCT k.tg_id FROM keys k WHERE k.expiry_time > EXTRACT(EPOCH FROM CURRENT_TIMESTAMP) ORDER BY k.tg_id;\""
    
    output, error, code = run_ssh_command(cmd)
    
    if code != 0:
        print(f"❌ Ошибка: {error}")
        return
    
    users = [line.strip() for line in output.strip().split('\n') if line.strip()]
    
    print(f"✅ Найдено {len(users)} пользователей с активными ключами")
    
    # Сохраняем в файл
    users_file = Path("users_with_active_keys.txt")
    
    with open(users_file, 'w', encoding='utf-8') as f:
        f.write("# Список пользователей с активными ключами\n")
        f.write("# Действующие ключи (expiry_time > current_timestamp)\n")
        f.write("# Получено из таблицы keys в bot_db через SSH\n")
        f.write("# Формат: tg_id\n")
        f.write("#\n")
        
        for user_id in users:
            f.write(user_id + "\n")
    
    print(f"\n{'='*70}")
    print("💾 ГОТОВО!")
    print("="*70)
    print(f"Сохранено {len(users)} пользователей")
    print(f"Файл: {users_file}")
    print(f"Размер: {users_file.stat().st_size} байт")
    print("="*70)


if __name__ == "__main__":
    main()
