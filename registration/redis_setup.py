import redis


def get_redis_instance():
    return redis.Redis(host='localhost', port=6379, db=0)
