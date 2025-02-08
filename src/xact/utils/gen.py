from datetime import datetime, timezone
from uuid import uuid4

from xact.config.gen import config


def gen_datetime(local_utc:bool=config.TIME_UTF_LOCAL):
    """give local_utc or utc time"""
    if not local_utc:
        return datetime.now(timezone.utc)
    return datetime.now()


def gen_uuid():
    """generate uuid"""
    return uuid4()
