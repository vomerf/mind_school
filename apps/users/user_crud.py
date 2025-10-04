from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.base_crud import CRUDBase
from apps.users.models import Pupil, User


class CRUDUser(CRUDBase):

    # Имя и Фамилия не уникальный поэтому для проверки нужно добавить email или phone
    async def check_user_exists(self, session: AsyncSession, **kwargs):
        stmt = select(
            exists().where(
                User.name == kwargs["name"], User.last_name == kwargs["last_name"]
            )
        )
        result = await session.execute(stmt)
        return result.scalar()


class CRUDPupil(CRUDUser):
    pass


crud_user = CRUDUser(User)
crud_pupil = CRUDPupil(Pupil)
