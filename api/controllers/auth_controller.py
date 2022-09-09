from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.utils import password_hash, jwt_encoder
from api import models, schema
from api.utils.database import get_db

router = APIRouter(
    prefix="/api/v1/auth"
)


@router.post('/register', response_model=schema.UserInfoOut, status_code=status.HTTP_201_CREATED)
async def register_user(user: schema.UserInfoIn, db: Session = Depends(get_db)):
    get_email = db.query(models.User).filter(models.User.email == user.email).first()
    if get_email:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=f"This{user.email} belongs to a user already")
    hashed_password = password_hash.hash_password(user.password)
    db_create_user = models.User(
        username=user.username.capitalize(),
        email=user.email.lower(),
        password=hashed_password
    )
    db.add(db_create_user)
    db.commit()
    db.refresh(db_create_user)
    return db_create_user


@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not password_hash.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = jwt_encoder.create_access_token(data={"user_id": user.id
                                                         })

    return {"access_token": access_token,
            "token_type": "bearer"
            }

