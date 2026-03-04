#!/usr/bin/env python3
"""
Mass Broadcast Bot - Main Entry Point
Authorizes, loads users, and broadcasts messages.
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from pyrogram import Client
from scripts.tg_client import build_client
from scripts.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, TELEGRAM_SESSION_NAME

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("broadcast.main")


def load_users_from_file(file_path="users_with_active_keys.txt"):
    """Load user list from file."""
    users = []
    path = Path(file_path)
    
    if not path.exists():
        logger.warning(f"⚠️ File {file_path} not found!")
        return users
    
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            try:
                user_id = int(line)
                users.append({'id': user_id, 'username': None})
            except ValueError:
                logger.warning(f"⚠️ Line {line_num}: Invalid ID '{line}' - skipped")
    
    logger.info(f"✅ Loaded {len(users)} users from {file_path}")
    return users


async def send_message(client, user_id, message_text, delay=5):
    """Send message to user with flood handling."""
    try:
        await client.send_message(
            chat_id=user_id,
            text=message_text,
            parse_mode="Markdown"
        )
        return True
    except Exception as e:
        logger.error(f"❌ Error sending to {user_id}: {e}")
        return False


async def broadcast(client, users, message, delay=5):
    """Broadcast message to all users."""
    total = len(users)
    
    if total == 0:
        logger.warning("⚠️ No users to broadcast to!")
        return
    
    print("\n" + "=" * 70)
    print("📢 STARTING MASS BROADCAST")
    print("=" * 70)
    print(f"👥 Recipients: {total}")
    print(f"📝 Message: {message[:100]}...")
    print(f"⏱️ Delay: {delay}s")
    print("=" * 70 + "\n")
    
    success_count = 0
    error_count = 0
    
    for i, user in enumerate(users, 1):
        user_id = user['id']
        
        print(f"[{i}/{total}] Sending to {user_id}...")
        
        success = await send_message(client, user_id, message, delay)
        
        if success:
            success_count += 1
        else:
            error_count += 1
        
        # Delay between messages (except after last)
        if i < total:
            await asyncio.sleep(delay)
        
        # Progress update
        if i % 25 == 0:
            print(f"\n📊 Progress: {i}/{total} ({i/total*100:.1f}%)")
    
    # Print statistics
    print("\n" + "=" * 70)
    print("📊 BROADCAST STATISTICS")
    print("=" * 70)
    print(f"Total recipients: {total}")
    print(f"✅ Success: {success_count}")
    print(f"❌ Errors: {error_count}")
    if total > 0:
        print(f"📈 Success rate: {success_count/total*100:.1f}%")
    print("=" * 70)


async def main():
    """Main entry point."""
    
    # Parse arguments
    import argparse
    
    parser = argparse.ArgumentParser(description="Mass Broadcast Bot")
    parser.add_argument('--message', '-m', type=str, required=True, help='Message to broadcast')
    parser.add_argument('--delay', '-d', type=int, default=5, help='Delay between messages (seconds)')
    parser.add_argument('--api-id', type=int, default=TELEGRAM_API_ID, help='Telegram API ID')
    parser.add_argument('--api-hash', type=str, default=TELEGRAM_API_HASH, help='Telegram API Hash')
    parser.add_argument('--phone', type=str, default=TELEGRAM_PHONE, help='Phone number')
    parser.add_argument('--users-file', type=str, default='users_with_active_keys.txt', help='Users file')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("📢 MASS BROADCAST BOT")
    print("=" * 70)
    print(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API ID: {args.api_id}")
    print(f"API Hash: {args.api_hash[:8]}...")
    print(f"Phone: {args.phone}")
    print(f"Users file: {args.users_file}")
    print(f"Message: {args.message[:50]}...")
    print("=" * 70)
    
    # Load users
    users = load_users_from_file(args.users_file)
    
    if not users:
        logger.error("❌ No users found!")
        print("\n💡 Create users file by running:")
        print("   python get_users_from_db.py")
        return
    
    # Create and start client
    client = build_client()
    
    try:
        print("\n📱 Connecting to Telegram...")
        await client.connect()
        print("✅ Connected!")
        
        # Get user info
        me = await client.get_me()
        print(f"\n✅ Authorized: @{me.username}")
        print(f"   Name: {me.first_name}")
        print(f"   Phone: {me.phone_number or 'N/A'}")
        
        # Broadcast
        await broadcast(client, users, args.message, args.delay)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Broadcast interrupted by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
    finally:
        await client.disconnect()
        print("\n🔌 Disconnected from Telegram")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
