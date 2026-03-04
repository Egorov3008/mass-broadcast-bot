#!/usr/bin/env python3
"""
Mass Broadcast Bot - Main Entry Point
Authorizes and runs mass message broadcasting.
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from scripts.tg_client import build_client
from scripts.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, TELEGRAM_SESSION_NAME

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("broadcast.main")


async def main():
    """Main entry point."""
    
    print("=" * 70)
    print("📢 MASS BROADCAST BOT")
    print("=" * 70)
    print(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API ID: {TELEGRAM_API_ID}")
    print(f"Session: {TELEGRAM_SESSION_NAME}")
    print("=" * 70)
    
    # Create client
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
        
        # Disconnect (authorization only)
        await client.disconnect()
        
        print("\n" + "=" * 70)
        print("✅ AUTHORIZATION SUCCESSFUL!")
        print("=" * 70)
        print("\n📝 To broadcast messages:")
        print("   python mass_broadcast.py --message 'Your message' --delay 5")
        print("\n" + "=" * 70)
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        await client.disconnect()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
