from datetime import datetime , timedelta
from fastapi import Depends, status, HTTPException 
from jose import JWTError , jwt
from fastapi.security import OAuth2PasswordBearer
import schema , database , models
from sqlalchemy.orm import Session 
# from config import setting
oauth2_scheme =  OAuth2PasswordBearer(tokenUrl='Login')


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORIHTM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    
    encode_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm= ALGORIHTM)
    return encode_jwt

# credentials_axception
def verify_access_token(token : str , credentials_axception ):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORIHTM])
        id : str = payload.get("user_id")
        if id is None : 
            print("Id" , id)
            raise  credentials_axception 
        
        token_data = schema.TokenData(id= id)
    except JWTError:
        print("Error Occured")
        raise credentials_axception
   
    
    return token_data

def get_current_user(token : str = Depends(oauth2_scheme) , db : Session = Depends(database.get_db)):

    print("Token===> ",token)
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentails", headers = {"WWW-Authenticate" : "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user