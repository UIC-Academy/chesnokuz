from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post
from app.utils import generate_slug
from app.schemas import PostCreateRequest, PostListResponse


app = FastAPI(
    title="Chesnokdek achchiq yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)


@app.get("/posts/", response_model=list[PostListResponse])
async def get_posts(is_active: bool = None, session: Session = Depends(get_db)):
    stmt = select(Post)

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    stmt = stmt.order_by(Post.created_at.desc())
    res = session.execute(stmt)
    return res.scalars().all()


@app.get("/post/{slug}/", response_model=PostListResponse)
async def get_post(slug: str, session: Session = Depends(get_db)):
    stmt = select(Post).where(Post.slug.like(f"%{slug}%"))
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@app.post("/post/create/")
async def post_create(
    create_data: PostCreateRequest, session: Session = Depends(get_db)
):
    post = Post(
        title=create_data.title,
        body=create_data.body,
        slug=generate_slug(create_data.title),
    )

    session.add(post)
    session.commit()
    session.refresh(post)

    return post


@app.put("/posts/{post_id}/")
async def post_update():
    pass


@app.patch("/posts/{post_id}/")
async def post_update_patch():
    pass


@app.delete("/posts/{post_id}/")
async def post_delete():
    pass


@app.deactivate("/posts/{post_id}/")
async def post_deactivate():
    pass
