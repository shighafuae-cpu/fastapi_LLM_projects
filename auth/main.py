from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models , schemas, utils
from auth_database import get_db
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

SECRET_KEY = "b6T_qD3AUnyASDX11LVS_gUSdA-BVLPFuhdzmO5p5jY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30

# Helper Function that takes user data
def create_access_token(data: dict): 
    to_encode = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({'exp' : expiry})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

app = FastAPI()

@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check the user exist or not 
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code = 400, detail= "Username already exist")
    
    # Hash the password 
    hashed_pass =  utils.hash_password(user.password)

    # Create new User Instance
    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_pass,
        role = user.role
    )

    # Save user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # return user excluding password 
    return {
        "id" : new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role
    }

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
    
    token_data = {'sub': user.username, 'role': user.role}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}



