# simple-job-queue

A simple job queue (FIFO) implementation using Redis.

## Prerequisites

ℹ️ NOTE: This setup is only tested on macOS.

Install Homebrew using [these instructions](https://brew.sh/)

### Python

Any version at or above Python 3.10 should work. Install it like so:

```shell
brew install python
```

### uv

Also install the Python package manager `uv` using the [official instructions](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

### Docker

Install Docker using [the official instructions](https://docs.docker.com/get-docker/).

## Setup

### Install dependencies

At the root of the project directory, run the following:

```shell
uv sync
```

### Environment variables

Copy the [sample env file](.env.sample) to `.env`. Set the environment variables as preferred.

## Running

To run this, navigate to the root of the project directory.

First, in a terminal session, we'll need to launch a Redis server to hold our job store and job queue.

Replace `{REDIS_PORT}` with the port you set in your `.env` file.

```shell
docker run --name redis -d -p {REDIS_PORT}:6379 redis:latest
```

Next, in a separate terminal session, we'll need to launch at least one job consumer. Feel free to repeat this step in different terminal sessions to launch more job consumers.

```shell
uv run consumer.py
```

Finally, in a separate terminal session, we'll need to launch a job producer.

```shell
uv run producer.py
```

Now we're all set!

Be sure to terminate the producer and consumer sessions when you're done, or else they'll keep running in the background!

### Sample output

```shell
$ uv run consumer.py
=== Job consumer ===

Starting job consumer. Polling every 1.0 seconds.
Press Ctrl+C to stop.
Currently there are 0 jobs waiting

No jobs in queue. Waiting...

Processing job: fe77ad78-5ae8-4abb-b306-96f1d8f2abdd
Payload: {'task_name': 'send_email', 'to': 'user7149@example.com', 'subject': 'Update_19'}
Performing task: send_email
Job fe77ad78-5ae8-4abb-b306-96f1d8f2abdd completed successfully
```

```shell
$ uv run producer.py
=== Job producer ===

Press Ctrl+C to stop.

Created job with ID: fe77ad78-5ae8-4abb-b306-96f1d8f2abdd

Created job with payload: {'task_name': 'send_email', 'to': 'user7149@example.com', 'subject': 'Update_19'}
Queue now has 1 job(s) waiting.
Created job with ID: 46948e68-afa1-456d-b974-0ac845da99e7

Created job with payload: {'task_name': 'risky_operation', 'should_fail': True, 'severity': 4}
Queue now has 1 job(s) waiting.
Created job with ID: 9f6c84db-f003-4962-8ecb-d858d4094ed2
```
