from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from apps.scores.crud.score_crud import score_crud


class ServiceScore:

    async def create_score_for_subject(
        self, score_in: BaseModel, session: AsyncSession
    ):
        return await score_crud.create(score_in, session)

    async def get_score_by_subject(self, subject: str, session: AsyncSession):
        return await score_crud.get_score_by_subject(subject, session)

    async def get_score(self, session: AsyncSession):
        return await score_crud.get_multi(session)

    async def update_score(
        self, score_id: int, score_in: BaseModel, session: AsyncSession
    ):
        score = await score_crud.get(score_id, session)
        score = await score_crud.update(score, score_in, session)
        return score
