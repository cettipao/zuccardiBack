from sqlalchemy.orm import Session
from models.users import User as UserModel
from schemas.users import User as UserSchema
from passlib.hash import sha256_crypt


def get_user(db: Session, user_id: int):

    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(UserModel).offset(skip).limit(limit).all()


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

def get_user_by_token(db: Session, token: str):
    return db.query(UserModel).filter(UserModel.token == token).first()


def create_user(db: Session, user: UserSchema):
    hashed_password = sha256_crypt.encrypt(user.password)
    db_user = UserModel(
        username=user.username,
        password=hashed_password,
        token=user.token,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
