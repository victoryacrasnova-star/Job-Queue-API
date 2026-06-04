from datetime import datetime, UTC
from sqlalchemy import Integer, Column, String, DateTime, JSON

from app.database import Base


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)

    # все что ниже - под вопросом

    type = Column(String, nullable=False) # тип задачи
    status = Column(String, nullable=False, default="queued") # статус
    payload = Column(JSON, nullable=False) # входные данные задачи
    result = Column(JSON) # результат выполнения
    error = Column(String) # текст ошибки
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC)) # время создания задачи
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)) # время последнего обновления задачи
