import collections
import functools
from collections import Counter

import requests

def LFUcache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            class LFUCache:
                def __init__(self, capacity):
                    self.cache = Counter()
                    self.capacity = capacity
                    self.recency = 0

                def get(self, key):
                    if key not in self.cache:
                        return -1
                    self.recency -= 1
                    self.cache[key] = [self.cache[key][0] - 1, self.recency, self.cache[key][2]]

                    return self.cache[key][2]

                def set(self, key, val):
                    if self.capacity:
                        self.recency -= 1

                        if key in self.cache:
                            self.cache[key] = [self.cache[key][0] - 1, self.recency, val]
                            return

                        if len(self.cache) == self.capacity:
                            k, _ = self.cache.most_common(1)[0]
                            print(k)
                            del self.cache[k]

                        self.cache[key] = [0, self.recency, val]

            return deco
        return internal

#@LFUcache
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


#print(fetch_url('https://www.google.com.ua/?hl=ru'))

#cache = LFUcache(2)
#cache.set(1, 1)
#cache.set(2, 2)
#print(cache.get(1))
#cache.set(3, 3)
#print(cache.get(2))
#print(cache.get(3))
#cache.set(4, 4)
#print(cache.get(1))
#print(cache.get(3))
#print(cache.get(4))
#cache.set(5, 5)
#print(cache.get(4))
#print(cache.get(5))
#print(cache.get(3))





