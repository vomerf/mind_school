from pydantic import BaseModel


class SubjectsBase(BaseModel):
    score: int
    subject_id: int
