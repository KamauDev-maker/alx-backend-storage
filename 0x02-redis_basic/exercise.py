#!/usr/bin/env python3
"""
Redis client module
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    Caching class
    """
    def __init__(self):
        """
        Initialize the Redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Method that takes a data args and returns a str
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
