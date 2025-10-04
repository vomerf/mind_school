from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.database import get_session
from apps.scores.logger import score_logger
from apps.scores.schemas.scores import ScoreCreate, ScoreDB, ScoreUpdate
from apps.scores.services.scores import ServiceScore

router = APIRouter(prefix="/scores", tags=["Scores"])


@router.post("/", response_model=ScoreDB)
async def create_score_for_subject(
    score_in: ScoreCreate,
    session: AsyncSession = Depends(get_session),
):
    return await ServiceScore().create_score_for_subject(score_in, session)


@router.get("/{subject_name}", response_model=list[ScoreDB])
async def get_score_by_subject(
    subject_name: str,
    session: AsyncSession = Depends(get_session),
):
    scores = await ServiceScore().get_score_by_subject(subject_name, session)
    if not scores:
        score_logger.info(f"Нет оценок по предмету {subject_name}")
    return scores


@router.get("/", response_model=list[ScoreDB])
async def get_score(
    session: AsyncSession = Depends(get_session),
):
    scores = await ServiceScore().get_score(session)
    if not scores:
        score_logger.info(f"Нет оценок")
    return scores


@router.put("/{score_id}", response_model=ScoreDB)
async def update_score(
    score_id: int,
    score_in: ScoreUpdate,
    session: AsyncSession = Depends(get_session),
):
    score = await ServiceScore().update_score(score_id, score_in, session)
    return score
