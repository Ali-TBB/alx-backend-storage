#!/usr/bin/env python3
""" Redis """
from typing import Callable, Optional, Union
import redis
import uuid


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
    
    def get(self, key: str, fn: Optional[Callable] = None):
            """
            Retrieves the value associated with the given key from Redis.

            Args:
                key (str): The key to retrieve the value for.
                fn (Optional[Callable]): An optional function to apply to the retrieved value.

            Returns:
                The retrieved value, or None if the key does not exist.

            """
            data = self._redis.get(key)
            
            if not data:
                return None
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