import os
import redis


class RedisWrapper(object):
    _instance = None

    def __init__(self):
        redis_host = os.getenv("REDIS_HOST")
        redis_port = os.getenv("REDIS_PORT")
        redis_db = os.getenv("REDIS_DB")

        if not redis_host:
            raise ValueError("REDIS_HOST is not set")

        if not redis_port:
            raise ValueError("REDIS_PORT is not set")

        if not redis_db:
            raise ValueError("REDIS_DB is not set")

        self.client = redis.Redis(
            host=redis_host,
            port=int(redis_port),
            db=int(redis_db),
            decode_responses=True,
        )

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
