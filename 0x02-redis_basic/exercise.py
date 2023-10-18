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

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, float, None]:
        """
        Method that takes a key str arg and optional callable arg fn
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Method that will parametrize cache.get
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Method that will automatically parametrize cache.get
        """
        return self.get(key, fn=int)
