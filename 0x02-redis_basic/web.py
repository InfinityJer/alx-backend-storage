# web.py
import redis
import requests
from functools import wraps
from typing import Callable

# Connect to Redis
redis_client = redis.Redis()


def cache_and_track(url: str, expiration_time: int = 10) -> Callable:
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Track the number of accesses to the URL
            count_key = f"count:{url}"
            redis_client.incr(count_key)

            # Check if the page is already cached
            cache_key = f"cache:{url}"
            cached_content = redis_client.get(cache_key)

            if cached_content is not None:
                return cached_content.decode("utf-8")

            # Fetch the page content using requests
            page_content = func(*args, **kwargs)

            # Cache the page content with expiration time
            redis_client.setex(cache_key, expiration_time, page_content)

            return page_content

        return wrapper

    return decorator

@cache_and_track(url="http://slowwly.robertomurray.co.uk/delay/5000/url/https://www.example.com")
def get_page(url: str) -> str:
    # Use requests to fetch the HTML content of the URL
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Example usage
    url_to_fetch = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://www.example.com"
    html_content = get_page(url_to_fetch)
    print(html_content)

    # Check the access count for the URL
    access_count_key = f"count:{url_to_fetch}"
    access_count = redis_client.get(access_count_key)
    print(f"The URL has been accessed {int(access_count)} times.")
