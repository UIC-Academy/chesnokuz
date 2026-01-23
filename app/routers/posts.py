from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Post
from app.database import get_db
from app.schemas import PostListResponse


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostListResponse])
async def get_posts(is_active: bool = None, session: Session = Depends(get_db)):
    stmt = select(Post)

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    stmt = stmt.order_by(Post.created_at.desc())
    res = session.execute(stmt)
    return res.scalars().all()
