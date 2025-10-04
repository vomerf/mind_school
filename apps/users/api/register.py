from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.database import get_session
from apps.users.schemas import UserCreate
from apps.users.services import ServicePupil

router = APIRouter(tags=["Users"])


# Пока что сделано под учеников, переделать для регистрации любого пользователя
@router.post(
    "/register-pupil/",
)
async def register_pupil(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
):

    return await ServicePupil().register_pupil(user, session)
