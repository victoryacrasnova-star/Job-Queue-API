import os

from dotenv import load_dotenv
from redis import Redis

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')
QUEUE_NAME = "jobs_queue"


if not REDIS_URL:
    raise ValueError('REDIS_URL is not set')

redis_client = Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)

def enqueue_job(job_id: int) -> None:
    redis_client.rpush(QUEUE_NAME, job_id)

def dequeue_job():
    job_id = redis_client.lpop(QUEUE_NAME)

    if job_id is None:
        return None

    return int(job_id)