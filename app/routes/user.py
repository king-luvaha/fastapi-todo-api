from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas, models, auth
from app.dependencies import get_db

router = APIRouter(tags=["Users"])


# -------- Register -------- #
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_username = db.query(models.User).filter(models.User.username == user.username).first()
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = auth.hash_password(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# -------- Login -------- #
@router.post("/login", response_model=schemas.Token)
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_login.email).first()

    if not user or not auth.verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": user.username})
    refresh_token = auth.create_refresh_token_db(user=user, db=db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# --------- Refresh Token ----------#
@router.post("/refresh-token", response_model=schemas.Token)
def refresh_token(req: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    username = auth.verify_refresh_token_db(req.refresh_token, db)
    user = db.query(models.User).filter_by(username=username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = auth.create_access_token(data={"sub": username})
    new_refresh_token = auth.create_refresh_token_db(user=user, db=db)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

# --------- Logout ----------#
@router.post("/logout")
def logout(req: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    token_entry = db.query(models.RefreshToken).filter_by(token=req.refresh_token).first()

    if not token_entry or token_entry.is_revoked:
        raise HTTPException(status_code=401, detail="Token already invalid or not found")

    token_entry.is_revoked = True
    db.commit()

    return {"detail": "Logged out successfully"}