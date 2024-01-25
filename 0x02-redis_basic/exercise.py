#!/usr/bin/env python3
'''Redis Cache Module
'''
from functools import wraps
from typing import Any, Callable, Union
import redis
import uuid

def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''returns the given method after incrementing its call counter.
        '''

        # Increment call counter in Redis
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.
        '''
        # Set up keys for storing input and output history
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        
        # Store input in Redis
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        
        # Execute the method and get its output
        output = method(self, *args, **kwargs)
        
        # Store output in Redis
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        
        return output
    
    return invoker

def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.
    '''
    # Check if the function has an associated Redis instance
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    
    # Check if the Redis instance is valid
    if not isinstance(redis_store, redis.Redis):
        return
    
    # Retrieve function name, input and output keys, and call count
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    
    # Display function call count
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    
    # Retrieve and display input and output history
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))

class Cache:
    '''Represents an object for storing data in a Redis data storage.
    '''

    def __init__(self) -> None:
        # Initialize Redis instance and flush the database
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data:  Union[str, bytes, int, float]) -> str:
        '''Stores a value in a Redis data storage and returns the key.
        '''
        # Generate a unique key for the data and store it in Redis
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Retrieves a value from a Redis data storage.
        '''
        # Retrieve data from Redis and apply conversion function if provided
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''Retrieves a string value from a Redis data storage.
        '''
        # Retrieve string data from Redis
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Retrieves an integer value from a Redis data storage.
        '''
        # Retrieve integer data from Redis
        return self.get(key, lambda x: int(x))
