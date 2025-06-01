import uuid
import random
import time
from datetime import datetime
from typing import Any

from dotenv import load_dotenv

from job_data import JobData, JobStatus
from job_queue import JobQueue
from job_store import JobStore


class JobProducer:
    """Handles creating jobs and pushing them to the queue."""

    def __init__(self, job_store: JobStore, job_queue: JobQueue):
        self.job_store = job_store
        self.job_queue = job_queue

    def create_job(self, payload: dict[str, Any]) -> str:
        """Create a new job and add it to the queue."""

        job_id = str(uuid.uuid4())

        job = JobData(
            id=job_id,
            status=JobStatus.PENDING,
            created_at=datetime.now(),
            payload=payload,
        )

        self.job_store.create_job(job)

        self.job_queue.push_job(job_id)

        print(f"Created job with ID: {job_id}")

        return job_id


def main():
    """Run the producer to continuously create random jobs."""

    print("=== Job producer ===\n")
    print("Press Ctrl+C to stop.\n")

    load_dotenv()

    job_store = JobStore()
    job_queue = JobQueue()

    producer = JobProducer(job_store, job_queue)

    # Function to generate random job payloads
    def get_random_job() -> dict[str, Any]:
        job_type = random.randint(1, 5)

        # Email Notification
        if job_type == 1:
            user_id = random.randint(1000, 9999)
            email = f"user{user_id}@example.com"
            subjects = ["Hello", "Welcome", "Notification", "Alert", "Update"]
            subject = f"{random.choice(subjects)}_{random.randint(1, 100)}"

            return {"task_name": "send_email", "to": email, "subject": subject}

        # Data Processing
        elif job_type == 2:
            file_id = random.randint(1, 1000)
            file_types = ["csv", "json", "xml", "txt"]
            file_path = f"/tmp/data_{file_id}.{random.choice(file_types)}"

            return {"task_name": "process_data", "file_path": file_path}

        # Failed Job
        elif job_type == 3:
            should_fail = random.choice([True, False])
            severity = random.randint(1, 5)

            return {
                "task_name": "risky_operation",
                "should_fail": should_fail,
                "severity": severity,
            }

        # Image Resizing
        elif job_type == 4:
            width = random.choice([800, 1024, 1280, 1920])
            height = random.choice([600, 768, 1080])
            quality = random.randint(70, 100)

            return {
                "task_name": "resize_image",
                "width": width,
                "height": height,
                "quality": quality,
            }

        # Database Backup
        else:
            db_names = ["users", "products", "orders", "payments", "logs"]
            db_name = random.choice(db_names)
            backup_type = random.choice(["full", "incremental", "differential"])

            return {
                "task_name": "backup_db",
                "db_name": db_name,
                "backup_type": backup_type,
            }

    created_count = 0

    try:
        while True:
            # Get a random job with already randomized payload
            payload = get_random_job()

            # Create the job
            producer.create_job(payload)
            created_count += 1

            print(f"\nCreated job with payload: {payload}")
            print(f"Queue now has {job_queue.get_job_count()} job(s) waiting.")

            # Wait for 1 second before creating the next job
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\nProducer stopped. Created {created_count} job(s) in total.")


if __name__ == "__main__":
    main()
