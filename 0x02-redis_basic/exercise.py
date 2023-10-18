#!/usr/bin/env python3
"""
Redis client module
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    count calls decorator takes a callable method as an arg
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Function that will replaxce the original method
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Method takes a decorator callable as an arg
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Function that will replace the original method
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result
    return wrapper


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

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Method that takes a data args and returns a str
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def replay(fn: Callable) -> None:
        """
        function that takes fn an arg
        """
        input_Key = f"{fn.__qualname__}:inputs"
        output_key = f"{fn.__qualname__}:outputs"

        input_history = [eval(args) for args in cache._redis.lrange(
            inputs_key, 0, -1)]
        output_history = cache._redis.lrange(output_key, 0, -1)
        print(f"{fn.__qualname__} was called {len(input_history)} times:")
        for args, output in zip(input_history, output_history):
            print(f"{fn.__qualname__}{args} -> {output.decode('utf-8')}")

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
