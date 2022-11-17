import functools
import collections
from collections import OrderedDict
import requests
import sys


def memory():
    def memory_lfu():
        a = str(sys.getsizeof(LFUCache))
        print(f'Memory:\t' + a)
    return memory_lfu()


class LFUCache:

    def __init__(self, capacity):
        self.remain = capacity
        self.least_freq = 1
        self.node_for_freq = collections.defaultdict(collections.OrderedDict)
        self.node_for_key = dict()

    def _update(self, key, value):
        _, freq = self.node_for_key[key]
        self.node_for_freq[freq].pop(key)
        if len(self.node_for_freq[self.least_freq]) == 0:
            self.least_freq += 1
        self.node_for_freq[freq + 1][key] = (value, freq + 1)
        self.node_for_key[key] = (value, freq + 1)

    def get(self, key):
        if key not in self.node_for_key:
            return -1
        value = self.node_for_key[key][0]
        self._update(key, value)
        return value

    def put(self, key, value):
        if key in self.node_for_key:
            self._update(key, value)
        else:
            self.node_for_key[key] = (value, 1)
            self.node_for_freq[1][key] = (value, 1)
            if self.remain == 0:
                removed = self.node_for_freq[self.least_freq].popitem(
                    last=False)
                self.node_for_key.pop(removed[0])
            else:
                self.remain -= 1
                self.least_freq = 1



def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content



#print(LFUCache('https://lms.ithillel.ua/'))
#print(fetch_url('https://lms.ithillel.ua/'))
#print(fetch_url('https://www.olx.ua/uk/'))
#print(fetch_url.__str__()('https://www.youtube.com/').replace('', ''),breakpoint())
#print(fetch_url('https://www.youtube.com/'))
#print(LFUCache)
#print(fetch_url('https://www.google.com.ua/?hl=ru'))
cache = LFUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))
cache.put(3, 3)
print(cache.get(2))
cache.put(4, 4)
print(cache.get(1))
print(cache.get(3))
print(cache.get(4))
#print(fetch_url('https://lms.ithillel.ua/'))
print(memory())