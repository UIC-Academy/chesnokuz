from .posts import router as posts_router
from .tag import router as tags_router
from .category import router as category_router
from .profession import router as profession_router
from .tmp import router as tmp_router

__all__ = [
    "posts_router",
    "tags_router",
    "category_router",
    "profession_router",
    "tmp_router",
]
