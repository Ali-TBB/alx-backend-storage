#!/usr/bin/env python3
""" Redis """
from typing import Union
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
