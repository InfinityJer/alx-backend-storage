#!/usr/bin/env python3
"""
Redis Cache Module
"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): Method to be decorated.

    Returns:
        Callable: Decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)  # Increment the count for the method's key
        return method(self, *args, **kwargs)
        # Call the original method and return its result

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.

    Args:
        method (Callable): Method to be decorated.

    Returns:
        Callable: Decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        # Append input arguments to the "...:inputs" list
        self._redis.rpush(inputs_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output in the "...:outputs" list
        self._redis.rpush(outputs_key, output)

        return output

    return wrapper


class Cache:
    """
    Cache class for storing, retrieving, counting method calls,
    and maintaining call history in Redis
    """

    def __init__(self):
        """
        Initialize the Cache with a Redis client and flush the instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.

        Args:
            data (Union[str, bytes, int, float]): Data to be stored.

        Returns:
            str: Generated random key used for storing the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None)
    -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis using the provided key
        and optionally apply a conversion function.

        Args:
            key (str): Key to retrieve data from Redis.
            fn (Callable, optional):
            Conversion function to apply to the retrieved data.

        Returns:
            Union[str, bytes, int, float]: Retrieved data.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve string data from Redis using the provided key.

        Args:
            key (str): Key to retrieve data from Redis.

        Returns:
            str: Retrieved string data.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve integer data from Redis using the provided key.

        Args:
            key (str): Key to retrieve data from Redis.

        Returns:
            int: Retrieved integer data.
        """
        return self.get(key, fn=int)

    def replay(self, method: Callable) -> None:
        """
        Display the history of calls for a particular function.

        Args:
            method (Callable): Method to display the history for.
        """
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        inputs = self._redis.lrange(inputs_key, 0, -1)
        outputs = self._redis.lrange(outputs_key, 0, -1)

        print("{} was called {} times:".
              format(method.__qualname__, len(inputs)))

        for inp, out in zip(inputs, outputs):
            print("{} -> {}".format(inp, out))

# Example usage


if __name__ == "__main__":
    cache = Cache()

    cache.store("foo")
    cache.store("bar")
    cache.store(42)

    cache.replay(cache.store)
