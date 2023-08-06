import json

from redis import Redis


class RedisKV(object):
    def __init__(self, host, port, db=0, hkey="kv", socket_timeout=5, socket_connect_timeout=5, decode_responses=True):
        self.db = Redis(host=host, port=port, db=db,
                        socket_timeout=socket_timeout, socket_connect_timeout=socket_connect_timeout,
                        decode_responses=decode_responses)
        self.hkey = hkey

    def get(self, k):
        res = self.db.hget(self.hkey, k)
        if not res:
            return dict()
        try:
            return json.loads(res)
        except:
            return dict()

    def set(self, k, v):
        v = json.dumps(v)
        self.db.hset(self.hkey, k, v)

    def ls(self):
        return self.db.hkeys(self.hkey)

    def delete(self, k):
        self.db.hdel(self.hkey, k)
