from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import List, Optional
from database import get_db
from schemas.post import PostCreate, PostUpdate, PostResponse
from models import Post, PostCategory, Category, User
from security import get_current_admin, get_current_user


router = APIRouter(prefix="/posts", tags=["Posts"])

# публичные эндпоинты, админские с: current_user: User = Depends(get_current_admin)

@router.get("/", response_model=List[PostResponse])
def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):

# запрос с подгрузкой автора и категорий
    query = db.query(Post).options(
        joinedload(Post.author),
        joinedload(Post.categories).joinedload(PostCategory.category)
    )
    
    if category_id:
        query = query.join(PostCategory).filter(PostCategory.cat_id == category_id)
    
    # сортировка по дате
    posts = query.order_by(desc(Post.created_at)).offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).options(
        joinedload(Post.author),
        joinedload(Post.categories).joinedload(PostCategory.category)
    ).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="категория не найдена"
        )
    return post

@router.get("/category/{category_id}", response_model=List[PostResponse])
def get_posts_by_category(
    category_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="категория не найдена"
        )
    
# посты с фильтром по категории
    posts = db.query(Post).options(
        joinedload(Post.author),
        joinedload(Post.categories).joinedload(PostCategory.category)
    ).join(PostCategory).filter(
        PostCategory.cat_id == category_id
    ).order_by(desc(Post.created_at)).offset(skip).limit(limit).all()
    
    return posts

# админские ендпоинты

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):

    new_post = Post(
        title=post.title,
        content=post.content,
        author_id=current_user.id  # автор текущий админ
    )
    db.add(new_post)
    db.flush()  # чтобы получить id поста
    
    if post.category_ids: # добавляем куатегории
        categories = db.query(Category).filter(Category.id.in_(post.category_ids)).all()
        if len(categories) != len(post.category_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="одна или несколько категорий не найдены"
            )
        
        for cat_id in post.category_ids:
            post_category = PostCategory(post_id=new_post.id, cat_id=cat_id)
            db.add(post_category)
    
    db.commit()
    
    created_post = db.query(Post).options(
        joinedload(Post.author),
        joinedload(Post.categories).joinedload(PostCategory.category)
    ).filter(Post.id == new_post.id).first()
    
    return created_post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="пост не найден"
        )

    if post_update.title is not None: # обновляем
        post.title = post_update.title
    if post_update.content is not None:
        post.content = post_update.content
    if post_update.category_ids is not None: # категории
        db.query(PostCategory).filter(PostCategory.post_id == post_id).delete() # удаляем старые
        
        if post_update.category_ids: # добавляем новые
            categories = db.query(Category).filter(Category.id.in_(post_update.category_ids)).all()
            if len(categories) != len(post_update.category_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="одна или несколько категорий не найдены"
                )
            
            for cat_id in post_update.category_ids:
                post_category = PostCategory(post_id=post_id, cat_id=cat_id)
                db.add(post_category)
    
    db.commit()
    
    # возвр. обновленный пост
    updated_post = db.query(Post).options(
        joinedload(Post.author),
        joinedload(Post.categories).joinedload(PostCategory.category)
    ).filter(Post.id == post_id).first()
    
    return updated_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="пост не найден"
        )
    
    db.delete(post)  # связи в posts_category удалятся автоматически
    db.commit()