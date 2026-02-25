from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter


from app.routers import (
    auth_router,
    posts_router,
    tags_router,
    category_router,
    profession_router,
    weather_router,
    users_router,
    lesson_router,
)
from app.exceptions import (
    zero_division_error_exc,
    AnasbekSleepyException,
    anasbek_sleepy_error_exc,
)
from app.admin.settings import admin
from app.middlewares import TimeCounterMiddleware


app = FastAPI(
    title="Chesnokdek achchiq yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)


app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(tags_router)
app.include_router(category_router)
app.include_router(profession_router)
app.include_router(weather_router)
app.include_router(users_router)
app.include_router(lesson_router)


app.add_exception_handler(ZeroDivisionError, zero_division_error_exc)
app.add_exception_handler(AnasbekSleepyException, anasbek_sleepy_error_exc)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

admin.mount_to(app=app)


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)  # DisallowedHost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)  # CORS
app.add_middleware(TimeCounterMiddleware)

app.state.limiter = limiter


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)
