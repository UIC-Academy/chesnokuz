from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_dep
from app.models import User
from app.schemas import UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile/", response_model=UserResponse)
async def get_profile(db: db_dep, email: str):
    stmt = select(User).where(User.email == email)
    res = db.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User Not found")

    return user
