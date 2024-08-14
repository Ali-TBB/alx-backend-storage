#!/usr/bin/env python3
""" Redis """
from typing import Callable, Optional, Union, Any
import redis
import uuid
from functools import wraps


def count_calls(method: callable) -> callable:
    """

    Args:
        method (callable): _description_

    Returns:
        callable: _description_
    """
    @wraps(method)
    def warpper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """ _description_
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return warpper

def call_history(method : callable) -> callable:
    """ _description_"""
    @wraps(method)
    def warpper(self:Any, *args:Any, **kwargs:Any) -> Any:
        """ _description_"""
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return warpper

class Cache:
    """
    A class that represents a cache using Redis.

    Attributes:
        _redis (redis.StrictRedis): The Redis client object.

    Methods:
        store(data): Stores the given data in the cache
        and returns the generated key.
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in the cache.

        Args:
            data: The data to be stored in the cache.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Retrieves the value associated with the given key from Redis.

        Args:
            key (str): The key to retrieve the value for.
            fn (Optional[Callable]): An optional function
            to apply to the retrieved value.

        Returns:
            The retrieved value, or None if the key does not exist.

        """
        client = self._redis
        data = client.get(key)
        if not data:
            return
        if fn is int:
            return self.get_int(data)
        if fn is str:
            return self.get_str(data)
        if Callable(fn):
            return fn(data)
        return data

    def get_str(self, data: bytes) -> str:
        """ Converts bytes to string
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """ Converts bytes to integers
        """
        return int(data)
