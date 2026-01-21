from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post


app = FastAPI(
    title="Chesnokdek achchiq yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)


@app.get("/posts/")
async def get_posts(session: Session = Depends(get_db)):
    stmt = select(Post).order_by(Post.created_at.desc())
    res = session.execute(stmt)
    return res.scalars().all()


@app.post("/post/create/")
async def post_create():
    pass
