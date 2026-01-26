from fastapi import FastAPI

from app.routers import posts_router
from app.routers import tags_router
from app.routers import category_router
from app.routers import profession_router
from app.routers import tmp_router


app = FastAPI(
    title="Chesnokdek achchiq yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)

app.include_router(posts_router)
app.include_router(tags_router)
app.include_router(category_router)
app.include_router(profession_router)
app.include_router(tmp_router)
