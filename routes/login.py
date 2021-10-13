from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from passlib.hash import sha256_crypt

from database.sqlalchemy import get_db
from schemas.users import User as UserSchema
from cruds.users import get_user, get_users, create_user, get_user_by_username, get_user_by_token
from client.loginClient import get_auth_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db),):
    user = get_user_by_token(db, token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="No puede iniciar sesión con el token proporcionado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/users/", response_model=List[UserSchema])
async def get_all_users(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    users = get_users(db, skip=skip, limit=limit)
    return users

"""
@router.post("/users/", response_model=UserSchema)
def post_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)
"""

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Busco el usuario en sqlite, si no esta lo busco en clima"""

    user_sqlite = get_user_by_username(db, username=form_data.username)
    if user_sqlite:
        if not sha256_crypt.verify(form_data.password, user_sqlite.password):
            raise HTTPException(
                status_code=400,
                detail="No puede iniciar sesión con las credenciales proporcionadas.",
            )
        else:
            return {"token": user_sqlite.token}
    else:
        response = get_auth_token(form_data.username, form_data.password)
        if response.status_code == 200:

            new_user = UserSchema(
                username=form_data.username,
                password=form_data.password,
                token=response.json()["token"],
            )

            create_user(db=db, user=new_user)

            return response.json()
        elif response.status_code == 400:
            raise HTTPException(
                status_code=400, detail=response.json()["non_field_errors"][0]
            )

    raise HTTPException(status_code=500, detail="Internal Server Error")
