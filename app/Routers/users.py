
from fastapi import FastAPI , Response, APIRouter ,status, HTTPException , Depends 
# from .. import models, schema, utils
import models, schema, utils
from database import  get_db
from sqlalchemy.orm import Session


router = APIRouter()
# router = APIRouter(prefix="/post", tags=["post"])
router = APIRouter()

@router.post('/create_user' , status_code=status.HTTP_201_CREATED , response_model= schema.UserOut)
def create_user( user : schema.UserCreate, db : Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}' , response_model= schema.UserOut)
async def get_user(id : int , db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail= f"user at {id} this id dose not exist")
    
    return user
