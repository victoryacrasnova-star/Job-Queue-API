from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import JobRead, JobCreate
from app.crud import create_job as create_job_crud
from app.crud import get_job as get_job_crud
from app.crud import list_jobs as list_jobs_crud
from app.redis_client import enqueue_job

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)) -> JobRead:
    job = create_job_crud(db, job_data)

    enqueue_job(job.id)

    return job

@router.get("",response_model=list[JobRead])
def get_jobs(db: Session = Depends(get_db)) -> list[JobRead]:
    return list_jobs_crud(db)

@router.get("/{job_id}", response_model=JobRead)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)) -> JobRead:
    job = get_job_crud(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found")

    return job