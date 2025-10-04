from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.database import get_session
from apps.scores.services.subjects import ServiceSubjects

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("/")
async def get_subjects(
    session: AsyncSession = Depends(get_session),
):
    subjects = await ServiceSubjects().get_subjects(session)
    return subjects
