from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine

with engine.connect() as connection:
    connection.execute(text("SELECT 1"))
app = FastAPI(title="Job Queue API")

@app.get("/health")
def health_check():
    return {"status": "ok"}