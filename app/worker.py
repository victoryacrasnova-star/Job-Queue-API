from app.crud import (
    get_job,
    set_job_status,
    set_job_result,
    set_job_error,
)

from app.redis_client import dequeue_job
from app.database import SessionLocal
from app.schemas import JobStatusEnum

def process_next_job():
    db = SessionLocal()

    try:
        job_id = dequeue_job()

        if job_id is None:
            return

        job = get_job(db, job_id)

        if job is None:
            return

        set_job_status(
            db,
            job,
            JobStatusEnum.processing,
        )

    finally:
        db.close()