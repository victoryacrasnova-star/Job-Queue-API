from fastapi import FastAPI

from app.routers import job

app = FastAPI(title="Job Queue API")
app.include_router(job.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}