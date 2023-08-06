import sys
import os
import signal
import json
from threading import Thread


def load(location, auto_dump, sig=True):
    return FedorDB(location, auto_dump, sig)


class FedorDB(object):

    key_string_error = TypeError('Key/name must be a string!')

    def __init__(self, location, auto_dump, sig):
        self.load(location, auto_dump)
        self.dthread = None
        if sig:
            self.set_sigterm_handler()

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __delitem__(self, key):
        return self.rem(key)

    def set_sigterm_handler(self):
        def sigterm_handler():
            if self.dthread is not None:
                self.dthread.join()
            sys.exit(0)
        signal.signal(signal.SIGTERM, sigterm_handler)

    def load(self, location, auto_dump):
        location = os.path.expanduser(location)
        self.loco = location
        self.auto_dump = auto_dump
        if os.path.exists(location):
            self._loaddb()
        else:
            self.db = {}
        return True

    def dump(self):
        json.dump(self.db, open(self.loco, 'wt'))
        self.dthread = Thread(
            target=json.dump,
            args=(self.db, open(self.loco, 'wt')))
        self.dthread.start()
        self.dthread.join()
        return True

    def _loaddb(self):
        try: 
            self.db = json.load(open(self.loco, 'rt'))
        except ValueError:
            if os.stat(self.loco).st_size == 0:  # Error raised because file is empty
                self.db = {}
            else:
                raise  # File is not empty, avoid overwriting it

    def _autodumpdb(self):
        if self.auto_dump:
            self.dump()

    def set(self, key, value):
        if isinstance(key, str):
            self.db[key] = value
            self._autodumpdb()
            return True
        else:
            raise self.key_string_error

    def get(self, key):
        try:
            return self.db[key]
        except KeyError:
            return False

    def getall(self):
        return self.db.keys()

    def exists(self, key):
        return key in self.db

    def rem(self, key):
        if not key in self.db: # return False instead of an exception
            return False
        del self.db[key]
        self._autodumpdb()
        return True

    def totalkeys(self, name=None):
        if name is None:
            total = len(self.db)
            return total
        else:
            total = len(self.db[name])
            return total

    def append(self, key, more):
        tmp = self.db[key]
        self.db[key] = tmp + more
        self._autodumpdb()
        return True

    def lcreate(self, name):
        if isinstance(name, str):
            self.db[name] = []
            self._autodumpdb()
            return True
        else:
            raise self.key_string_error

    def ladd(self, name, value):
        self.db[name].append(value)
        self._autodumpdb()
        return True

    def lextend(self, name, seq):
        self.db[name].extend(seq)
        self._autodumpdb()
        return True

    def lgetall(self, name):
        return self.db[name]

    def lget(self, name, pos):
        return self.db[name][pos]

    def lrange(self, name, start=None, end=None):
        return self.db[name][start:end]

    def lremlist(self, name):
        number = len(self.db[name])
        del self.db[name]
        self._autodumpdb()
        return number

    def lremvalue(self, name, value):
        self.db[name].remove(value)
        self._autodumpdb()
        return True

    def lpop(self, name, pos):
        value = self.db[name][pos]
        del self.db[name][pos]
        self._autodumpdb()
        return value

    def llen(self, name):
        return len(self.db[name])

    def lappend(self, name, pos, more):
        tmp = self.db[name][pos]
        self.db[name][pos] = tmp + more
        self._autodumpdb()
        return True

    def lexists(self, name, value):
        return value in self.db[name]

    def dcreate(self, name):
        if isinstance(name, str):
            self.db[name] = {}
            self._autodumpdb()
            return True
        else:
            raise self.key_string_error

    def dadd(self, name, pair):
        self.db[name][pair[0]] = pair[1]
        self._autodumpdb()
        return True

    def dget(self, name, key):
        return self.db[name][key]

    def dgetall(self, name):
        return self.db[name]

    def drem(self, name):
        del self.db[name]
        self._autodumpdb()
        return True

    def dpop(self, name, key):
        value = self.db[name][key]
        del self.db[name][key]
        self._autodumpdb()
        return value

    def dkeys(self, name):
        return self.db[name].keys()

    def dvals(self, name):
        return self.db[name].values()

    def dexists(self, name, key):
        return key in self.db[name]

    def dmerge(self, name1, name2):
        first = self.db[name1]
        second = self.db[name2]
        first.update(second)
        self._autodumpdb()
        return True

    def deldb(self):
        self.db = {}
        self._autodumpdb()
        return True