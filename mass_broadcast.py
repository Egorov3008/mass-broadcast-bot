#!/usr/bin/env python3
"""
Массовая рассылка сообщений через Pyrogram
Использует локальный список пользователей
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from pyrogram import Client
from pyrogram.errors import FloodWait, UserBlocked, PeerIdInvalid

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("broadcast")


class BroadcastClient:
    """Клиент для массовых рассылок"""
    
    def __init__(
        self,
        api_id: int,
        api_hash: str,
        phone_number: str,
        users_file: str = "/root/.openclaw/workspace/users_with_active_keys.txt"
    ):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.users_file = users_file
        
        self.client = None
        self.users: List[Dict[str, Any]] = []
        self.stats = {
            'total': 0,
            'sent': 0,
            'failed': 0,
            'blocked': 0
        }
        
        # Создаем сессию
        self.session_path = Path("/root/.openclaw/media/telegram_sessions/broadcast_client2_session")
    
    async def connect(self) -> bool:
        """Подключение к Telegram"""
        try:
            logger.info("📱 Инициализация клиента...")
            
            self.client = Client(
                name=self.session_path.name,
                api_id=self.api_id,
                api_hash=self.api_hash,
                phone_number=self.phone_number,
                workdir=str(self.session_path.parent),
                device_model="Broadcast Client 2",
                app_version="1.0",
                system_version="Linux"
            )
            
            await self.client.connect()
            logger.info("✅ Подключено к Telegram")
            
            # Проверяем авторизацию
            me = await self.client.get_me()
            logger.info(f"✅ Авторизован: @{me.username} ({me.id})")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка подключения: {e}")
            return False
    
    async def disconnect(self):
        """Отключение от Telegram"""
        if self.client:
            await self.client.disconnect()
            logger.info("🔌 Отключено от Telegram")
    
    def load_users_from_file(self) -> List[Dict[str, Any]]:
        """Загрузка пользователей из файла"""
        users_path = Path(self.users_file)
        
        if not users_path.exists():
            logger.warning(f"⚠️ Файл {self.users_file} не найден")
            logger.info("📝 Создаю тестовый список пользователей")
            return self._get_test_users()
        
        users = []
        
        with open(users_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue
                
                try:
                    # Формат: user_id username (опционально)
                    parts = line.split()
                    user_id = int(parts[0])
                    username = parts[1] if len(parts) > 1 else None
                    
                    users.append({
                        'id': user_id,
                        'username': username,
                        'name': None
                    })
                    
                except (ValueError, IndexError) as e:
                    logger.warning(f"⚠️ Строка {line_num}: {line} - пропущена")
                    continue
        
        logger.info(f"✅ Загружено {len(users)} пользователей из {self.users_file}")
        
        if not users:
            logger.warning("⚠️ Список пользователей пуст")
            return self._get_test_users()
        
        return users
    
    def _get_test_users(self) -> List[Dict[str, Any]]:
        """Тестовые пользователи"""
        return [
            {'id': 123456789, 'username': '@test_user_1', 'name': 'Test User 1'},
            {'id': 987654321, 'username': '@test_user_2', 'name': 'Test User 2'},
            {'id': 111222333, 'username': '@test_user_3', 'name': 'Test User 3'},
        ]
    
    async def send_message(
        self,
        message_text: str,
        user_id: int,
        parse_mode: str = "Markdown"
    ) -> bool:
        """Отправка сообщения пользователю"""
        try:
            await self.client.send_message(
                chat_id=user_id,
                text=message_text,
                parse_mode=parse_mode
            )
            
            self.stats['sent'] += 1
            logger.info(f"✅ Сообщение отправлено пользователю {user_id}")
            return True
            
        except FloodWait as e:
            wait_time = e.x
            logger.warning(f"⏳ FloodWait: {wait_time} секунд. Ждем...")
            await asyncio.sleep(wait_time)
            # Повторная попытка
            return await self.send_message(message_text, user_id)
            
        except UserBlocked:
            self.stats['blocked'] += 1
            logger.warning(f"🚫 Пользователь {user_id} заблокировал бота")
            return False
            
        except PeerIdInvalid:
            self.stats['failed'] += 1
            logger.warning(f"❌ Пользователь {user_id} не найден")
            return False
            
        except Exception as e:
            self.stats['failed'] += 1
            logger.error(f"❌ Ошибка отправки пользователю {user_id}: {e}")
            return False
    
    async def broadcast(self, message: str, delay: int = 5):
        """Массовая рассылка"""
        logger.info("=" * 60)
        logger.info("📢 НАЧАЛО МАССОВОЙ РАССЫЛКИ")
        logger.info("=" * 60)
        logger.info(f"👥 Получателей: {len(self.users)}")
        logger.info(f"📝 Сообщение: {message[:100]}...")
        logger.info(f"⏱️ Задержка: {delay} сек")
        logger.info("=" * 60)
        
        self.stats['total'] = len(self.users)
        
        start_time = datetime.now()
        
        for i, user in enumerate(self.users, 1):
            user_id = user['id']
            username = user.get('username', '') or ''
            
            logger.info(f"[{i}/{self.stats['total']}] Отправка {username} (ID: {user_id})")
            
            # Отправляем сообщение
            success = await self.send_message(message, user_id)
            
            # Пауза между сообщениями
            if i < len(self.users):
                await asyncio.sleep(delay)
        
        # Вывод статистики
        self._print_stats()
    
    def _print_stats(self):
        """Вывод статистики рассылки"""
        elapsed = datetime.now()
        logger.info("=" * 60)
        logger.info("📊 СТАТИСТИКА РАССЫЛКИ")
        logger.info("=" * 60)
        logger.info(f"Всего получателей: {self.stats['total']}")
        logger.info(f"✅ Отправлено: {self.stats['sent']}")
        logger.info(f"🚫 Заблокировано: {self.stats['blocked']}")
        logger.info(f"❌ Ошибки: {self.stats['failed']}")
        logger.info(f"Успешно: {(self.stats['sent'] / self.stats['total'] * 100):.1f}%")
        logger.info(f"⏱️ Время работы: {elapsed - datetime.now() if hasattr(self, 'start_time') else 'N/A'}")
        logger.info("=" * 60)


async def main():
    """Основная функция"""
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="Массовая рассылка сообщений через Pyrogram")
    
    # Telegram credentials
    parser.add_argument('--api-id', type=int, 
                       help='Telegram API ID',
                       default=os.getenv('TELEGRAM_API_ID', '36442196'))
    
    parser.add_argument('--api-hash', type=str,
                       help='Telegram API Hash',
                       default=os.getenv('TELEGRAM_API_HASH', '2c764877adb42800cb5f7af9252f2990'))
    
    parser.add_argument('--phone', type=str,
                       help='Телефон для авторизации',
                       default=os.getenv('TELEGRAM_PHONE', '+79322490462'))
    
    # Сообщение для рассылки
    parser.add_argument('--message', type=str, required=True,
                       help='Текст сообщения для рассылки')
    
    # Задержка между сообщениями
    parser.add_argument('--delay', type=int, default=5,
                       help='Задержка между сообщениями (секунды)')
    
    # Файл с пользователями (дефолт - только с активными ключами)
    parser.add_argument('--users-file', type=str,
                       help='Путь к файлу с пользователями',
                       default='/root/.openclaw/workspace/users_with_active_keys.txt')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("📢 MASS BROADCAST SCRIPT")
    logger.info("=" * 60)
    logger.info(f"API ID: {args.api_id}")
    logger.info(f"API Hash: {args.api_hash[:8]}...")
    logger.info(f"Телефон: {args.phone}")
    logger.info(f"Файл пользователей: {args.users_file}")
    logger.info(f"Сообщение: {args.message[:50]}...")
    logger.info("=" * 60)
    
    # Проверяем наличие файла
    users_path = Path(args.users_file)
    if users_path.exists():
        user_count = users_path.stat().st_size // 12
        logger.info(f"✅ Файл найден: {user_count} пользователей")
    else:
        logger.warning(f"⚠️ Файл не найден: {args.users_file}")
    
    # Создаем клиент
    client = BroadcastClient(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone_number=args.phone,
        users_file=args.users_file
    )
    
    try:
        # Подключаемся к Telegram
        if not await client.connect():
            logger.error("❌ Не удалось подключиться к Telegram")
            return
        
        # Загружаем пользователей
        client.users = client.load_users_from_file()
        
        if not client.users:
            logger.error("❌ Пользователи не найдены")
            return
        
        # Запускаем рассылку
        await client.broadcast(args.message, delay=args.delay)
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Рассылка остановлена пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
