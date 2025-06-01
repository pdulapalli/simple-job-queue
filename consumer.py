import random
import time
import signal
from datetime import datetime
from typing import Any

from dotenv import load_dotenv

from job_data import JobStatus
from job_queue import JobQueue
from job_store import JobStore


def task_handler(task_name: str, **kwargs: dict[str, Any]):
    print(f"Performing task: {task_name}")

    # Simulate work
    time.sleep(random.randint(2, 10))

    # Check for simulated failure
    if kwargs.get("should_fail"):
        raise Exception("Oh no, an error occurred!")


class JobConsumer:
    """Consumes jobs one at a time from the queue."""

    def __init__(self, job_store: JobStore, job_queue: JobQueue):
        self.job_store = job_store
        self.job_queue = job_queue
        self.running = False

    def process_job(self, job_id: str):
        job = self.job_store.get_job(job_id)
        if not job:
            print(f"Error: Job {job_id} not found in store")
            return

        print(f"\nProcessing job: {job_id}")
        print(f"Payload: {job.payload}")

        self.job_store.update_job_status(job_id, JobStatus.IN_PROGRESS)
        self.job_store.set_job_started_at(job_id, datetime.now())

        try:
            task_name = job.payload.pop("task_name", "unknown")

            task_handler(task_name, **job.payload)
        except Exception as e:
            self.job_store.update_job_status(job_id, JobStatus.FAILED)
            print(f"Job {job_id} failed: {str(e)}")

            return

        self.job_store.update_job_status(job_id, JobStatus.COMPLETED)
        self.job_store.set_job_completed_at(job_id, datetime.now())
        print(f"Job {job_id} completed successfully")

    def run(self, poll_interval_sec: float = 1.0):
        """Run the consumer in a loop, processing jobs as they come in."""

        self.running = True

        # Set up signal handling for graceful shutdown
        def handle_signal(sig, frame):
            print("\nShutting down consumer...")
            self.running = False

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        print(f"Starting job consumer. Polling every {poll_interval_sec} seconds.")
        print("Press Ctrl+C to stop.")
        print(f"Currently there are {self.job_queue.get_job_count()} jobs waiting")

        jobs_processed = 0

        waiting_in_empty = False

        while self.running:
            job_id = self.job_queue.pull_next_job()
            if job_id:
                waiting_in_empty = False
                self.process_job(job_id)
                jobs_processed += 1
            else:
                if not waiting_in_empty:
                    print("\nNo jobs in queue. Waiting...")

                waiting_in_empty = True
                time.sleep(poll_interval_sec)

        print(f"\nConsumer stopped after processing {jobs_processed} jobs")


def main():
    """Run the consumer to process jobs from the queue."""

    print("=== Job consumer ===\n")

    load_dotenv()

    job_store = JobStore()
    job_queue = JobQueue()
    consumer = JobConsumer(job_store, job_queue)

    consumer.run()


if __name__ == "__main__":
    main()
