from sqlalchemy.orm import Session
from models.user import User,User_Detail
from schemas.user import UserDetail,UserBase,UserDetailUpdate,UserUpdate
from utils.utils import get_password_hash
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

def get_user_by_id(db:Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db:Session, email:str):
    return db.query(User).filter(User.email == email).first()

def get_users(db:Session,skip:int = 0, limit:int=100):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
    
def create_user(db:Session, user:UserBase):
    if user.password != user.confirm_password:
        return (False,"Missing Password!")
    if get_user_by_email(db=db,email=user.email):
        return(False,"Email already registered!")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(email = user.email,password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return (True,db_user)

def update_user_by_id(db:Session, id:int,user:UserUpdate):
    exists_user = get_user_by_id(db=db, user_id=id)
    new_user = user.dict(exclude_unset=True)
    for key,value in new_user.items():
        setattr(exists_user,key,value)
    db.commit()
    db.refresh(exists_user)
    return exists_user

def check_create_user_detail(db:Session,user_id:int):
    user_detail = get_user_detail_by_id(db=db,user_id=user_id)
    if user_detail is None: 
        return False
    return True
    
def get_user_detail_by_id(db:Session, user_id:int):
    return db.query(User_Detail).filter(User_Detail.user_id==user_id).first()

def create_user_detail(db:Session,user_id:int, user_detail:UserDetail):
    if get_user_detail_by_id(db=db,user_id=user_id):
        raise HTTPException(status_code=404, detail="User Detail already exists.")
    user_detail = User_Detail(user_id=user_id,**user_detail.dict())
    db.add(user_detail)
    db.commit()
    db.refresh(user_detail)
    return user_detail

def update_user_detail(db:Session,user_id:int, user_detail:UserDetailUpdate):
    exists_user_detail = get_user_detail_by_id(db=db, user_id=user_id)
    if exists_user_detail is None:
        raise HTTPException(status_code=404, detail="User Detail not found!")
    user_detail_new = user_detail.dict(exclude_unset=True)
    for key,value in user_detail_new.items():
        setattr(exists_user_detail,key,value)
    db.commit()
    db.refresh(exists_user_detail)
    return exists_user_detail