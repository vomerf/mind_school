from fastapi import FastAPI

from apps.scores.api.endpoints.score import router as score_router
from apps.scores.api.endpoints.subjects import router as subjetc_router
from apps.users.api.register import router as user_router
from apps.core.test_user import create_test_user

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await create_test_user()


app.include_router(score_router)
app.include_router(user_router)
app.include_router(subjetc_router)
