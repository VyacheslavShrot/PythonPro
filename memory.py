import functools
import collections
from collections import OrderedDict
import requests
import sys
import psutil


def disk(f):
    def disk_lfu():
        a = str(psutil.virtual_memory())
        print(f'Disk:\t' + a)
    return disk_lfu()





def memory(f):
    def memory_lfu():
        a = str(sys.getsizeof(cache()))
        print(f'Memory:\t' + a)
    return memory_lfu()





def cache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in deco._cache:
                # переносимо в кінець списку
                deco._cache.move_to_end(cache_key, last=True)
                print(deco._cache)
                return deco._cache[cache_key]
            result = f(*args, **kwargs)
            # видаляємо якшо досягли ліміта
            if len(deco._cache) >= max_limit:
                 # видаляємо перший елемент
                deco._cache.popitem(last=False)
            deco._cache[cache_key] = result
            print(deco._cache)
            return result
        deco._cache = OrderedDict()
        return deco
    return internal


#@memory
#@disk
@cache(max_limit=5)
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content

print(fetch_url('https://www.google.com.ua/?hl=ru'))
#print(fetch_url('https://lms.ithillel.ua/'))
#print(fetch_url('https://www.olx.ua/uk/'))
#print(fetch_url('https://www.google.com.ua/?hl=ru'))
#print(fetch_url('https://www.youtube.com/'))
#print(fetch_url('https://www.youtube.com/'))

