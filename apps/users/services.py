from typing import Generic

from sqlalchemy.ext.asyncio import AsyncSession

from apps.base_crud import CreateSchemaType
from apps.users.user_crud import crud_pupil, crud_user


class ServiceUser(Generic[CreateSchemaType]):

    async def register_user(self, user: CreateSchemaType, session: AsyncSession):
        if await crud_user.check_user_exists(
            session, name=user.name, last_name=user.last_name
        ):
            print("Пользователь с таким именем и фамилией уже зарегестрирован")
            # Можно выкинуть кастомную ошибку
            raise
        new_user = await crud_user.create(user, session)
        return new_user


class ServicePupil(ServiceUser):
    async def register_pupil(self, user: CreateSchemaType, session: AsyncSession):
        if await crud_user.check_user_exists(
            session, name=user.name, last_name=user.last_name
        ):
            print("Пользователь с таким именем и фамилией уже зарегестрирован")
            # Можно выкинуть кастомную ошибку
            raise
        new_user = await crud_pupil.create(user, session)
        return new_user
