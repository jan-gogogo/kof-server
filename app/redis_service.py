import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
rds = redis.Redis(connection_pool=pool)


def set(key, val):
    rds.set(key, val)


def get(key):
    return rds.get(key)


def remove(key):
    return rds.delete(key)
