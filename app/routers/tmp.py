from enum import Enum
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Path, Query, Body, Cookie
from pydantic import BaseModel, Field


router = APIRouter(prefix="/tmp", tags=["tmp"])


class ItemRequest(BaseModel):
    id: int = Field(gt=0, lt=100)
    name: str
    is_active: bool


class TypeRequest(BaseModel):
    id: int = Field(gt=0, lt=100)
    name: str
    created_at: datetime


class ItemTypeEnum(str, Enum):
    # SUM type - aynan 1 tasi, bir nechtasi bir vaqtda emas
    ELECTRONIC = "electronic"
    CLOTHING = "clothing"
    GROCERY = "grocery"
    BOOK = "book"


@router.get("/t1/{item_type}/")
async def tmp(item_type: ItemTypeEnum):
    return {"item_type": item_type}


@router.get("/t2/{item_id}/")
async def tmp2(item_id: int = Path(gt=0, lt=100)):
    return {"item_id": item_id}


@router.get("/t3/")
async def tmp3(item_id: int = Query(gt=0, lt=100)):
    return {"item_id": item_id}


@router.post("/t4/{item_id}/")
async def tmp4(is_active: bool, item: ItemRequest, item_id: int = Path(gt=0, lt=100)):
    return {"item_id": item_id, "is_active": is_active, "item": item}


@router.post("/t5/")
async def tmp5(item: ItemRequest, type: TypeRequest):
    return {"item": item, "type": type}


"""
GET /users/1/?is_active=true HTTP/2\r\n
Accept: application/json\r\n
Accept-Language: en-US\r\n
Connection: keep-alive\r\n
Content-Length: 56\r\n\r\n
{
    "id": 1
}
"""


@router.put("/t6/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }


class ThemeEnum(str, Enum):
    LIGHT = "light"
    DARK = "dark"


@router.get("/t7/items/")
async def read_items(theme: Annotated[ThemeEnum | None, Cookie()] = None):
    return {"theme": theme}
