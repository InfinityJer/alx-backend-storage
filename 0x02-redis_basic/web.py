#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        # Increment the access count for the URL
        redis_store.incr(f'count:{url}')

        # Retrieve cached result from Redis
        result = redis_store.get(f'result:{url}')

        # return cached reults; otherwise, fetch and cache result
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)  # Reset access count
        redis_store.setex(f'result:{url}', 10, result)  
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    # Fetch the HTML content of the URL using requests
    return requests.get(url).text
