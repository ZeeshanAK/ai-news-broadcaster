"""
Database delivery log model.
Tracks delivery of broadcasts to various channels.
"""
from datetime import datetime
from enum import Enum


class DeliveryChannel(str, Enum):
    TELEGRAM = "telegram"
    EMAIL = "email"
    RSS = "rss"
    PODCAST = "podcast"


class DeliveryStatus(str, Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"


class DeliveryLog:
    """
    Delivery log model placeholder.
    Tracks broadcast delivery to channels.
    """
    
    # Fields
    id: int
    broadcast_id: int
    channel: DeliveryChannel
    status: DeliveryStatus
    recipient: str
    delivered_at: datetime
    error_message: str
    created_at: datetime