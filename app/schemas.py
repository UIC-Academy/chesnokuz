from datetime import datetime

from pydantic import BaseModel


class PostCreateRequest(BaseModel):
    title: str
    body: str


class PostListResponse(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    is_active: bool
    created_at: datetime


class PostUpdateRequest(BaseModel):
    title: str | None = None
    body: str | None = None
    is_active: bool | None = None


class TagCreateRequest(BaseModel):
    name: str
    slug: str


class TagUpdateRequest(BaseModel):
    name: str | None = None


class TagListResponse(BaseModel):
    id: int
    name: str
    slug: str


class CategoryListResonse(BaseModel):
    id: int | None = None
    name: str | None = None


class CategoryCreateRequest(BaseModel):
    name: str | None = None


class ProfessionCreateRequest(BaseModel):
    name: str


class ProfessionListResponse(BaseModel):
    id: int
    name: str


class ProfessionUpdateRequest(BaseModel):
    name: str
