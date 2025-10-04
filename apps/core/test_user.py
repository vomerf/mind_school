from sqlalchemy.ext.asyncio import AsyncSession
from apps.core.database import async_engine
from apps.users.models import User
# from apps.telegram_bot.main import TEST_USER_ID
from apps.core.config import settings


async def create_test_user():
    async with AsyncSession(async_engine) as session:
        result = await session.get(User, settings.TEST_USER_ID)
        if not result:
            user = User(
                name="test_user",
                last_name="test_user",
                phone='8999999999'
            )
            session.add(user)
            await session.commit()
            print("Test user created!")
        else:
            print("Test user already exists.")
