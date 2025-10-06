import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from apps.core.config import settings
from apps.core.database import Base, get_session
from apps.main import app

engine = create_async_engine(
    settings.DATABASE_URL_asyncpg,
    connect_args={"server_settings": {"search_path": "test_schema"}},
    future=True,
)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture(scope="function")
async def session_db():
    # создаём схему test_schema, если её нет
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS test_schema;"))
        await conn.run_sync(Base.metadata.create_all)
    try:
        async with async_session() as session:
            yield session
    finally:
        # после теста удаляем все таблицы только в test_schema
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest_asyncio.fixture
async def client(session_db):
    # переопределяем get_session так, чтобы тесты использовали test_schema
    app.dependency_overrides[get_session] = lambda: session_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()



@pytest.mark.asyncio
class TestScoresAPI:

    async def test_get_subjects(self, client):
        resp = await client.get("/subjects/")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        if data:  # если база не пустая
            assert "name" in data[0]
            assert "id" in data[0]

    async def test_get_scores_by_subject(self, client):
        resp = await client.get("/scores/math")
        assert resp.status_code in (200, 404)

        if resp.status_code == 200:
            data = resp.json()
            assert isinstance(data, list)
            if data:
                assert "value" in data[0]
                assert "subject_id" in data[0]

    async def test_update_score(self, client):
        # сначала создаём запись
        payload = {"subject_id": 1, "score": 3, 'user_id': 1}
        create_resp = await client.post("/scores/", json=payload)
        assert create_resp.status_code == 200
        created_score = create_resp.json()

        # теперь обновляем её
        update_payload = {"score": 4}
        update_resp = await client.put(f"/scores/{created_score['id']}", json=update_payload)

        # проверки
        assert update_resp.status_code == 200
        updated_score = update_resp.json()
        assert updated_score["value"] == 4
