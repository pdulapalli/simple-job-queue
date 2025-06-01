from datetime import datetime
from job_data import JobData, JobStatus
from redis_wrapper import RedisWrapper

JOB_DATA_KEY_PREFIX = "job_data"


class JobStore:
    def __init__(self):
        self._redis = RedisWrapper.get_instance()

    def _get_job_key(self, job_id: str) -> str:
        return f"{JOB_DATA_KEY_PREFIX}:{job_id}"

    def create_job(self, job_data: JobData) -> None:
        self._redis.client.hset(
            name=self._get_job_key(job_data.id),
            mapping=job_data.model_dump(mode="json", exclude_none=True),
        )

    def get_job(self, job_id: str) -> JobData | None:
        job_data = self._redis.client.hgetall(name=self._get_job_key(job_id))
        if not job_data:
            return None

        return JobData.model_validate(job_data)

    def update_job_status(self, job_id: str, status: JobStatus) -> None:
        self._redis.client.hset(
            name=self._get_job_key(job_id),
            key="status",
            value=status.value,
        )

    def set_job_started_at(self, job_id: str, started_at: datetime) -> None:
        self._redis.client.hset(
            name=self._get_job_key(job_id),
            key="started_at",
            value=started_at.isoformat(),
        )

    def set_job_completed_at(self, job_id: str, completed_at: datetime) -> None:
        self._redis.client.hset(
            name=self._get_job_key(job_id),
            key="completed_at",
            value=completed_at.isoformat(),
        )
