import time

import httpx

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

        try:

            if job.type == "site_check":
                url = job.payload.get("url")
                if not url:
                    raise ValueError("url is required for site_chek job")

                response = httpx.get(url, timeout=10)
                result = {
                    "status_code": response.status_code,
                }
            else:
                raise ValueError(f"Unknown job type: {job.type}")

            set_job_result(db, job, result)

            set_job_status(db,
                           job,
                           JobStatusEnum.done)

        except Exception as error:
            set_job_error(db, job, str(error))
            set_job_status(db,
                           job,
                           JobStatusEnum.failed)
    finally:
        db.close()

if __name__ == "__main__":
    while True:
        process_next_job()
        time.sleep(2)