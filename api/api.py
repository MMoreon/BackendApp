from fastapi import APIRouter
from api.v1 import auth, users, categories, posts

router = APIRouter(prefix="/v1")

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(categories.router)
router.include_router(posts.router)