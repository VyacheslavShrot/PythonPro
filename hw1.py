import functools
from collections import OrderedDict, Counter
#from distutils.command.install import key

import requests


def LFUcache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache = Counter()
            recency = 0


            if key not in cache:
                return -1
            recency -= 1
            cache[key] = [cache[key][0] - 1, recency, cache[key][2]]
            return cache[key][2]

            if capacity:
                recency -= 1
                if key in cache:
                    cache[key] = [cache[key][0] - 1, recency, val]
                    return


                if len(cache) == capacity:
                    k, _ = cache.most_common(1)[0]
                    print(k)
                    del cache[k]

                cache[key] = [0, recency, val]
                return deco



def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content