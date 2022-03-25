from typing import List, Optional
from fastapi import FastAPI , Response, status, HTTPException , Depends , APIRouter
# from .. import models, schema
# from .. import models, schema
import models, schema , Oauth2
from database import  get_db
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter()



# @router.get("/sqlalchemy")
# def test_posts(db : Session = Depends(get_db)):
#     posts  = db.query(models.Posts).all()
#     return {"data" : posts}

# @router.get("/posts")
@router.get("/posts" , response_model=List[schema.PostOut])
async def get_posts(db : Session = Depends(get_db) , current_user : int = Depends(Oauth2.get_current_user)
 , Limit : int = 10 , skip : int = 0 , search : Optional[str] = ""): 
    # return {"posts": my_posts}
    # posts = cursor.query(models.Posts).all()
    
    # return all posts from the DB
    posts  = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(Limit).offset(skip).all()
  
    results = db.query(models.Posts , func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Posts.id , isouter= True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(Limit).offset(skip).all()
    print("results : ",results)
    # this statment will give us only the loged in user post
    # posts  = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()
    return results

@router.get('/post/latest' , response_model= schema.PostOut)
async def get_latest_post(db : Session = Depends(get_db) , current_user : int = Depends(Oauth2.get_current_user)):
    my_posts = db.query(models.Posts , func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Posts.id , isouter= True).group_by(models.Posts.id).all()
    post = my_posts[len(my_posts)-1]
    return  post

@router.get("/post/{id}", response_model= List[schema.PostOut])
async def  get_post(id : int, db  :Session = Depends(get_db) , current_user : int = Depends(Oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post = cursor.fetchone()
    # print(post)
    # post = find_post(id)
    # post = db.query(models.Posts).filter(models.Posts.id == id).all()
    post = db.query(models.Posts , func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Posts.id , isouter= True).group_by(models.Posts.id).filter(models.Posts.id == id).all()
    print("Post : ",post)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"post with {id} ID was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with  {id} id was not found"}
    return post

@router.delete('/posts/{id}' , status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int , db : Session = Depends(get_db) , current_user : int = Depends(Oauth2.get_current_user)):
    # index = find_index_post(id)
    # cursor.execute(""" DELETE FROM posts WHERE id = %s  RETURNING * """ , (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Posts).filter(models.Posts.id == id)
     
    post = deleted_post.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail=f"post with Id : {id} dose not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Uthorized to perform this action")
    
    # my_posts.pop(index)
    # return {'message' : 'Post was successfully deleted'}
    deleted_post.delete(synchronize_session= False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)

# response_model= schema.Post
@router.post('/create_post', status_code= status.HTTP_201_CREATED, response_model= schema.Post)
async def Create_post(post :schema.PostCreate , db : Session = Depends(get_db),
  current_user = Depends(Oauth2.get_current_user)):

    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,10000)
    # my_posts.append(post_dict)
    # print(post)

    # cursor.execute(""" INSERT INTO posts (title , content , published) VALUES(%s , %s , %s) RETURNING *""" , (post.title , post.content , post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Posts(title = post.title , content = post.content , published = post.published)
    
    new_post = models.Posts(owner_id = current_user.id , **post.dict())
    # add new data to database
    db.add(new_post)
    # save changes 
    db.commit()
    # get current post  from db 
    db.refresh(new_post)
    return new_post

# Update data
@router.put('/post/{id}')
def Update_post(id : int, post : schema.PostCreate, db : Session =Depends(get_db) , current_user : int = Depends(Oauth2.get_current_user)):
    

    # index = find_index_post(id)
    # cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s  WHERE id = %s    RETURNING *""" , (post.title , post.content , post.published , str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post_query = db.query(models.Posts).filter(models.Posts.id == id)
    updated_post = updated_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="post with id : {id} dose not exist")
   
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Uthorized to perform this action")
    

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict 
    updated_post_query.update(post.dict(), synchronize_session= False)
    db.commit()
    return {'data' : updated_post_query.first()}