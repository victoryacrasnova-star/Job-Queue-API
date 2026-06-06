from typing import Any

from sqlalchemy.orm import Session
from app.models import Job
from app.schemas import JobCreate, JobStatusEnum

def create_job(db: Session, job_data: JobCreate) -> Job:
    job = Job(
        type=job_data.type,
        payload=job_data.payload,
        status=JobStatusEnum.queued.value,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job

def get_job(db: Session, job_id: int) -> Job | None:
    return db.query(Job).filter(Job.id == job_id).first()

def list_jobs(db: Session) -> list[Job]:
    return db.query(Job).all()

def set_job_status(db: Session, job: Job, status: JobStatusEnum) -> Job:
    job.status = status.value

    db.commit()
    db.refresh(job)

    return job

def set_job_result(db: Session, job: Job, result: dict[str, Any]) -> Job:
    job.result = result

    db.commit()
    db.refresh(job)

    return job

def set_job_error(db: Session, job: Job, error: str) -> Job:
    job.error = error

    db.commit()
    db.refresh(job)
    return job