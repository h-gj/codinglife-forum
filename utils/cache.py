import config
import memcache

mc = memcache.Client([config.CACHE_HOST], debug=True)


def set(key, value, timeout=120):
    return mc.set(key, value, timeout)


def get(key):
    return mc.get(key)
