from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app import schemas, models
from app.config import settings
from app.models import User
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.dependencies import get_db
import uuid

# SECRET and Algorithm for JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

REFRESH_SECRET_KEY = settings.REFRESH_SECRET_KEY
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme (used in protected routes)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# -------- Password Hashing -------- #

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# -------- JWT Token Handling -------- #

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception()
        return schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception()

def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


# -------- Get Current User -------- #

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    token_data = decode_access_token(token)
    user = db.query(User).filter(User.username == token_data.username).first()
    if not user:
        raise credentials_exception()
    return user

# -------- Refresh Token Creation -------- #

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception()
        return schemas.TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
def create_refresh_token_db(user: models.User, db: Session):
    raw_token = str(uuid.uuid4())
    encoded_token = jwt.encode({"sub": user.username}, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = models.RefreshToken(
        token=encoded_token,
        user_id=user.id,
        expires_at=expires_at,
        is_revoked=False
    )

    db.add(refresh_token)
    db.commit()
    return encoded_token

def verify_refresh_token_db(token: str, db: Session):
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    token_entry = db.query(models.RefreshToken).filter(models.RefreshToken.token == token).first()

    if not token_entry or token_entry.is_revoked or token_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired or revoked")

    return username


