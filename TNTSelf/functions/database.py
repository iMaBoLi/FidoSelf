from redis import Redis
from TNTSelf import config
import json, os

def get_data(self, key):
    data = self.get(str(key))
    if data:
        try:
            data = eval(data)
        except BaseException:
            pass
    return data

class RedisDB:
    def __init__(self):
        URL = (config.REDIS_URL).split(":")[0]
        PORT = (config.REDIS_URL).split(":")[-1]
        self.db = Redis(
                host=URL,
                password=config.REDIS_PASSWORD,
                port=int(PORT),
                decode_responses=True,
                socket_timeout=5,
                retry_on_timeout=True,
           )
        self.set = self.db.set
        self.get = self.db.get
        self.keys = self.db.keys
        self.ping = self.db.ping
        self.delete = self.db.delete
        self.recache()

    def recache(self):
        self.cache = {}
        for keys in self.keys():
            self.cache.update({keys: self.get_key(keys)})

    @property
    def all(self):
        self.recache()
        cache = json.dumps(self.cache, sort_keys=True, indent=4)
        return cache

    def set_key(self, key, value):
        value = str(value)
        try:
            value = eval(value)
        except BaseException:
            pass
        self.cache.update({key: value})
        return self.set(str(key), str(value))

    def get_key(self, key):
        if key in self.cache:
            return self.cache[key]
        get = get_data(self, key)
        self.cache.update({key: get})
        return get

    def del_key(self, key):
        if key in self.cache:
            del self.cache[key]
        return bool(self.delete(str(key)))
        
    def clean(self):
        for x in self.keys():
            self.del_key(x)
        return True

class Database:
    def __init__(self):
        self.dbname = "../tmp/TNTDB.json"
        self.cache = {}
        self.re_data()

    def get_data(self):
        if os.path.isfile(self.dbname):
            fdata = open(self.dbname, "r")
            data = fdata.read()
        else:
            data = str({})
            ndata = open(self.dbname, "w")
            ndata.write(data)
        return data

    def re_data(self):
        data = self.get_data()
        self.cache = eval(self.get_data()) if isinstance(data, str) else data

    def get(self, key):
        if key in self.cache:
            return self.cache.get(key)

    def set(self, key=None, value=None, delete_key=None):
        data = self.cache
        if delete_key:
            try:
                del data[delete_key]
            except KeyError:
                pass
        if key and value:
            data.update({key: value})
        with open(self.dbname, "w") as dbfile:
            json.dump(data, dbfile)
        self.re_data()
        return True

    def delete(self, key):
        if key in self.cache:
            return self.set(delete_key=key)

class LocalDB:
    def __init__(self):
        self.db = Database()
        self.get = self.db.get
        self.set = self.db.set
        self.delete = self.db.delete
        self.cache = {}
        self.recache()

    def keys(self):
        return []
        
    def recache(self):
        self.cache.clear()
        for key in self.keys():
            self.cache.update({key: self.get_key(key)})

    def get_data(self, key=None, data=None):
        if key:
            data = self.get(str(key))
        if data and isinstance(data, str):
            try:
                data = eval(data)
            except:
                pass
        return data

    def set_key(self, key, value):
        value = self.get_data(data=value)
        self.cache[key] = value
        return self.set(str(key), str(value))

    def del_key(self, key):
        if key in self.cache:
            del self.cache[key]
        self.delete(key)
        return True

    def get_key(self, key):
        if key in self.cache:
            value = self.cache[key]
        else:
            value = self.get_data(key)
            self.cache.update({key: value})
        try:
            data = eval(value)
        except:
            data = value
        return data

DB = LocalDB()
