#!/usr/bin/env python3
"""
Quick authorizer script for Mass Broadcast Bot.
Enter SMS code from Telegram to authorize.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pyrogram import Client


# Import config
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, TELEGRAM_SESSION_NAME

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("broadcast.authorizer")


async def main():
    """Main authorizer function."""
    
    print("=" * 70)
    print("🔐 MASS BROADCAST BOT - AUTHORIZER")
    print("=" * 70)
    print(f"API ID: {TELEGRAM_API_ID}")
    print(f"API Hash: {TELEGRAM_API_HASH[:8]}...")
    print(f"Phone: {TELEGRAM_PHONE}")
    print(f"Session: {TELEGRAM_SESSION_NAME}")
    print("=" * 70)
    
    # Create client
    client = Client(
        name=TELEGRAM_SESSION_NAME,
        api_id=TELEGRAM_API_ID,
        api_hash=TELEGRAM_API_HASH,
        phone_number=TELEGRAM_PHONE,
        workdir="sessions",
        device_model="Mass Broadcast Client",
        app_version="1.0",
        system_version="Linux"
    )
    
    print("\n📱 Connecting to Telegram...")
    try:
        await client.connect()
        print("✅ Connected!")
        
        # Check if already authorized
        me = await client.get_me()
        print(f"\n✅ Already authorized: @{me.username}")
        print(f"   Name: {me.first_name}")
        print(f"   Phone: {me.phone_number or 'N/A'}")
        print("\n💡 Bot is ready for broadcasting!")
        await client.disconnect()
        return
        
    except Exception as e:
        if "PHONE_CODE_INVALID" in str(e) or "SESSION_PASSWORD_NEEDED" in str(e):
            logger.info(f"❌ Authentication error: {e}")
            await client.disconnect()
            return
        elif "PHONE_CODE_HASH_MISSING" in str(e) or "PHONE_CODE" in str(e):
            pass  # Expected, we need to send code
        else:
            logger.error(f"❌ Connection error: {e}")
            await client.disconnect()
            return
    
    print("\n📱 Sending authorization request...")
    try:
        # Send code request (automatically handled by Pyrogram)
        await client.send_code(TELEGRAM_PHONE)
        print(f"\n📱 Check your phone {TELEGRAM_PHONE} for the code!")
        print("   Code will be sent via SMS or Telegram app")
        
        # Read code from user
        sms_code = input("\n📲 Enter SMS code: ").strip()
        
        if not sms_code:
            print("❌ No code entered!")
            await client.disconnect()
            return
        
        # Verify code
        print("⏳ Verifying code...")
        await client.sign_in(TELEGRAM_PHONE, sms_code)
        
        # Get user info
        me = await client.get_me()
        print(f"\n✅ SUCCESS! Authorized as: @{me.username}")
        print(f"   Name: {me.first_name}")
        print(f"   Phone: {me.phone_number or 'N/A'}")
        
        # Save session info
        session_info = {
            "username": me.username,
            "name": f"{me.first_name} {me.last_name or ''}",
            "phone": me.phone_number,
            "api_id": TELEGRAM_API_ID,
            "phone_number": TELEGRAM_PHONE
        }
        
        # Write to file
        info_file = Path("sessions_info.json")
        import json
        with open(info_file, 'w') as f:
            json.dump(session_info, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Session info saved to: {info_file}")
        print("=" * 70)
        print("✅ Authorizer complete!")
        print("✅ Bot is ready for mass broadcasting!")
        print("=" * 70)
        
    except Exception as e:
        logger.error(f"❌ Authorization error: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
