"""Utils for caching functions."""
import hashlib
import json
import os
import threading
from functools import wraps

CACHE_DIR = '/tmp/cache'


class _Cache:
    """Implements base cache logic.

    Data is cached both in memory and, for persistance, on disk. On *get*
    requests, memory is first inspected. If cache key is not found there,
    disk is inspected.

    Args:
        cache_name(str): Name to identify cache.

    Note:
        Used by decorator *cache* (See below).

    """

    @staticmethod
    def __get_hash(cache_key):
        return hashlib.md5(cache_key.encode()).hexdigest()

    __dir = '/tmp/cache'
    __store = {}
    __lock_map_lock = threading.Lock()
    __lock_map = {}
    __cache_name = 'new_cache'

    def __init__(self, cache_name):
        """Implement class constructor."""
        self.__cache_name = cache_name
        os.system('mkdir -p %s' % self.__get_dir())

    def __get_dir(self):
        return '%s/%s' % (CACHE_DIR, self.__cache_name)

    def __get_lock(self, key):
        # pylint: disable=R1732
        self.__lock_map_lock.acquire()
        if key not in self.__lock_map:
            self.__lock_map[key] = threading.Lock()
        lock = self.__lock_map[key]
        self.__lock_map_lock.release()
        return lock

    def __acquire_lock(self, key):
        self.__get_lock(key).acquire()

    def __release_lock(self, key):
        self.__get_lock(key).release()

    def __get_cache_file_name(self, cache_key):
        return '%s/%s' % (
            self.__get_dir(),
            _Cache.__get_hash(cache_key),
        )

    def __get_file_exists(self, key):
        return os.path.exists(self.__get_cache_file_name(key))

    def __get_from_file(self, key):
        with open(self.__get_cache_file_name(key)) as fin:
            data_json = fin.read()
            fin.close()

        if data_json == '':
            return None
        content = json.loads(data_json)
        return content

    def __set(self, key, data):
        self.__acquire_lock(key)
        with open(self.__get_cache_file_name(key), 'w') as fout:
            fout.write(json.dumps(data, ensure_ascii=True))
            fout.close()
        self.__store[key] = data
        self.__release_lock(key)

    def get(self, key_or_list, fallback):
        """Get data from cache if cache key exists, if not from fallback.

        Args:
            key_or_list (str or list): the cache key can be given as a string,
                or a list of strings, which are joined
            fallback (function): function to call of cache key not in cache

        Returns:
            data

        """
        if isinstance(key_or_list, list):
            key = ':'.join(key_or_list)
        else:
            key = key_or_list

        if key in self.__store:
            data = self.__store[key]
            return data

        if self.__get_file_exists(key):
            data = self.__get_from_file(key)
            if data is not None:
                self.__store[key] = data
                return data

        data = fallback()
        if data is not None:
            self.__set(key, data)
        return data

    def flush_store(self):
        """Flush all cache."""
        self.__store = {}

    def flush(self, key):
        """Flush cache for a given cache key.

        Args:
            key (str): Cache key to flush
        """
        self.__acquire_lock(key)
        if self.__get_file_exists(key):
            os.remove(self.__get_cache_file_name(key))
        if key in self.__store:
            del self.__store[key]
        self.__release_lock(key)


def cache(cache_name):
    """Wrap class Cache as decorator.

    Args:
        cache_name (str): cache name

    .. code-block:: python

        from utils.cache import cache

        @cache('test')
        def long_operation():
            import time
            time.sleep(100)
            return 1

        >>> long_operation() # takes >100s to run
        >>> long_operation() # runs almost instantly

    """

    def cache_inner(func):

        @wraps(func)
        def cache_inner_inner(*args, **kwargs):
            cache_key = json.dumps({
                'cache_name': cache_name,
                'function_name': func.__name__,
                'kwargs': kwargs,
                'args': args,
            })

            def fallback():
                return func(*args, **kwargs)

            return _Cache(cache_name).get(cache_key, fallback)

        return cache_inner_inner
    return cache_inner
