from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..sql import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/post",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def getpost(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,search:Optional[str]= ""):
    # x = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # x = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    x = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return x


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createpost(posts: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=posts.title,content=posts.body,published=posts.publish)
    new_post = models.Post(owner_id=current_user.id, **posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    index_query = db.query(models.Post).filter(models.Post.id == id)
    index = index_query.first()
    if index == None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="not found")
    if index.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    index_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, posts: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    update_post = db.query(models.Post).filter(models.Post.id == id)
    index = update_post.first()
    if index == None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="not found")
    if index.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    update_post.update(posts.dict(), synchronize_session=False)
    db.commit()
    return update_post.first()
