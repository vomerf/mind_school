from datetime import datetime

from pydantic import BaseModel


class ScoreBase(BaseModel):
    score: int
    subject_id: int


class ScoreCreate(ScoreBase):
    user_id: int | None = None


class ScoreUpdate(BaseModel):
    score: int | None = None


class ScoreDB(ScoreBase):
    id: int
    user_id: int
    date_entered: datetime
    date_updated: datetime

    class Config:
        from_attributes = True
