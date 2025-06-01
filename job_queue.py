from redis_wrapper import RedisWrapper

JOB_QUEUE_KEY = "job_queue"


class JobQueue:
    def __init__(self):
        self._redis = RedisWrapper.get_instance()

    def push_job(self, job_id: str) -> None:
        self._redis.client.lpush(
            JOB_QUEUE_KEY,
            job_id,
        )

    def pull_next_job(self) -> str | None:
        return self._redis.client.rpop(name=JOB_QUEUE_KEY)

    def peek_next_job(self) -> str | None:
        return self._redis.client.lindex(name=JOB_QUEUE_KEY, index=-1)

    def get_job_count(self) -> int:
        return self._redis.client.llen(name=JOB_QUEUE_KEY)
