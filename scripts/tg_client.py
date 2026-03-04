#!/usr/bin/env python3
"""
Create and return a Pyrogram client for mass broadcast.
"""

import logging
from pyrogram import Client
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION_NAME

logger = logging.getLogger("broadcast.client")


def build_client():
    """Create and return a Pyrogram client."""
    app = Client(
        name=TELEGRAM_SESSION_NAME,
        api_id=int(TELEGRAM_API_ID),
        api_hash=TELEGRAM_API_HASH,
        workdir="sessions",  # Directory for session files
        device_model="Mass Broadcast Client",
        app_version="1.0",
        system_version="Linux"
    )
    logger.info(f"Created Pyrogram client with session {TELEGRAM_SESSION_NAME}")
    return app
