from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from apps.base_crud import CRUDBase
from apps.scores.models import Score, Subject


class ScoreCRUD(CRUDBase):

    async def get_score_by_subject(self, subject: str, session: AsyncSession):
        stmt = (
            select(Subject)
            .options(selectinload(Subject.scores))
            .where(Subject.name == subject)
        )
        result = await session.execute(stmt)
        subject = result.scalar_one_or_none()
        if not subject:
            return None
        return subject.scores

    async def create_score_for_subject(self, subject: str, session: AsyncSession):
        pass

    async def update_score(self):
        pass


score_crud = ScoreCRUD(Score)
