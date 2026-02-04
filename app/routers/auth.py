from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select

from app.database import db_dep
from app.models import User
from app.schemas import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserLoginRequest,
    UserProfileResponse,
)
from app.utils import hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["Authentication"])


basic = HTTPBasic()


@router.post("/register/", response_model=UserRegisterResponse)
async def register_user(db: db_dep, data: UserRegisterRequest):
    stmt = select(User).where(User.email == data.email)
    res = (db.execute(stmt)).scalars().first()

    if res:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(email=data.email, password_hash=hash_password(data.password))

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login/")
async def login_user(
    db: db_dep,
    # data: UserLoginRequest,
    credentials: Annotated[HTTPBasicCredentials, Depends(basic)],
):
    print(">>>", credentials.username, credentials.password)
    stmt = select(User).where(User.email == credentials.username)
    user = (db.execute(stmt)).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user


@router.get("/profile/", response_model=UserProfileResponse)
async def user_profile(db: db_dep):
    pass


"""
Basic Auth - Payment system integration, very small setups
Session Auth - Django admin, some APIs, stateful
Token Auth (JWT) - industry standard, stateless
"""

"""
Basic Authentication -> username, password (Authorization: Basic)
JWT Auth -> Authorization: Bearer

1. Browser so'radi username-password
2. Browser uni o'zi Base64 ga o'girdi, yoniga Basic so'zini qo'ydi: Basic <base64_token>
3. Browser tokenni Authorization headerda jo'natdi
4. Request serverga keldi
5. HTTPBasic va HTTPBasicCredentials tokenni oldi, o'zi decode qildi va ma'lumotni chiqarib berdi
6. Biz username, password ishlata olamiz.

"username:password" -> base64
"""


"""
API -> Authorization: Basic ko'rinishidagi data kelishini talab qilyapti
"""
