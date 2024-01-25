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
    def invoker(url: str) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text


if __name__ == "__main__":
    # Example usage
    url_to_fetch = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://www.example.com"
    html_content = get_page(url_to_fetch)
    print(html_content)

    # Check the access count for the URL
    access_count_key = f"count:{url_to_fetch}"
    access_count = redis_store.get(access_count_key)
    print(f"The URL has been accessed {int(access_count)} times.")
