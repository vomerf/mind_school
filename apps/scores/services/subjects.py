from sqlalchemy.ext.asyncio import AsyncSession

from apps.scores.crud.subject_crud import subject_crud


class ServiceSubjects:
    async def get_subjects(self, session: AsyncSession):
        return await subject_crud.get_multi(session)
