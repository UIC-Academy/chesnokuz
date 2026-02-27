from typing import Annotated
from pathlib import Path
import shutil
import asyncio

from fastapi import APIRouter, Header, HTTPException, Form, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
from sqlalchemy import select

from app.database import db_dep
from app.config import settings
from app.models import User, Media
from app.exceptions import AnasbekSleepyException


router = APIRouter(prefix="/lesson", tags=["Lesson"])

SECRET_TOKEN = "shamsiddin"


@router.get("/protected/")
async def protected_api(
    db: db_dep, email: str, X_chesnok_token: Annotated[str | None, Header()] = None
):
    if not X_chesnok_token:
        raise HTTPException(status_code=401, detail="No chesnok token provided.")

    if X_chesnok_token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Incorrect chesnok token.")

    stmt = select(User).where(User.email == email)
    res = db.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@router.get("/protected/adminonly/")
async def protected_admin(
    db: db_dep, email: str, X_chesnok_token: Annotated[str | None, Header()] = None
):
    if not X_chesnok_token:
        raise HTTPException(status_code=401, detail="No chesnok token provided.")

    if X_chesnok_token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Incorrect chesnok token.")

    stmt = select(User).where(User.email == email)
    res = db.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="San mani adminimmassan karochi!")

    return user


@router.post("/testlogin/")
async def test_login(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    return {"username": username, "password": password}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile, db: db_dep):
    if file.size > 1024 * 1024 * 1:
        raise HTTPException(
            status_code=400, detail="File size is too large. Max size is 1MB."
        )

    file_ext = Path(file.filename).suffix.lower()  # image.png
    if file_ext not in [".jpg", ".png", ".jpeg"]:
        raise HTTPException(
            status_code=400,
            detail="File type is not supported. Only .jpg, .png, .jpeg are allowed.",
        )
    path = Path(settings.MEDIA_PATH)
    path.mkdir(exist_ok=True)
    res = path / file.filename  # chesnokuz/media/filename.jpg
    with open(res, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = Media(url=f"{settings.MEDIA_PATH}/{file.filename}")
    db.add(image)
    db.commit()
    db.refresh(image)

    return {"media_id": image.id, "url": f"{settings.BASE_URL}/{image.url}"}


@router.get("/exc/")
async def test_exception():
    raise AnasbekSleepyException("Why are you sleeping?")


@router.get("/htmlres/", response_class=HTMLResponse)
async def html_resp():
    return "<h1>HTML Response</h1>"


@router.websocket("/ws/")
async def test_ws(ws: WebSocket):
    await ws.accept()

    while True:
        await ws.send_text("Eshmat!")
        await asyncio.sleep(1)
