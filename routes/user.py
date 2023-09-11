from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import Response,RequestUser,RequestUserDetail,RequestUserDetailUpdate,UserOut,RequestUserUpdate,UserUpdate
from service.user import get_user_by_id,get_users,create_user,get_user_detail_by_id,create_user_detail,get_user_by_email,update_user_detail,update_user_by_id
from service.auth import get_current_active_user
from utils.utils import get_db
from service.auth import validate_token
from models.user import User
from pydantic import parse_obj_as


router = APIRouter(
    prefix="/user",
    responses={404: {"description": "Not found"}},
)

# User
@router.post("/", tags=['User'])
async def create_an_user(request:RequestUser,db:Session = Depends(get_db)):
    status,db_user = create_user(db=db, user=request.parameter)
    if status:
        return Response(code="200",status="OK",message="Success create User").dict(exclude_none=True)
    else: return Response(code="400",status="Failure",message=db_user)

@router.get("/",dependencies=[Depends(validate_token)], tags=['User'])
async def read_all_user(skip: int = 0,limit:int = 100, db:Session=Depends(get_db)):
    users = get_users(db=db,skip=skip,limit=limit)
    users_output = [UserOut(**x.__dict__) for x in users]
    return Response(code="200",status="OK",message="Success read all User",result=users_output)

@router.get("/{id}",dependencies=[Depends(validate_token)], tags=['User'])
async def read_user_by_id(id:int, db:Session= Depends(get_db)):
    db_user = get_user_by_id(db=db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User is non-existent.")
    user_out = UserOut(**db_user.__dict__)
    return Response(code="200", status="OK", message="Success read User",result=user_out)

@router.patch("/{id}",dependencies=[Depends(validate_token)], tags=['User'])
async def update_user(id:int,request:RequestUserUpdate,db:Session=Depends(get_db)):
    user_updated = update_user_by_id(id=id,db=db,user=request.parametr)
    user_updated_out = UserOut(**user_updated.__dict__)
    return Response(code="200",status="OK",message="Success Update User",result=user_updated_out).dict(exclude_none=True)

# Profile
@router.post("/profile/",dependencies=[Depends(validate_token)],tags=["Profile"])
async def create_profile_me(request:RequestUserDetail,current_user: User = Depends(get_current_active_user), db:Session = Depends(get_db)):
    create_user_detail(user_detail=request.parameter,user_id=current_user.id,db=db)
    update_user_by_id(db=db,id=current_user.id,user=UserUpdate(is_profile=True))
    return Response(code="200",status="OK",message="Success Create User Detail").dict(exclude_none=True)

@router.get("/profile/",dependencies=[Depends(validate_token)],tags=["Profile"])
async def read_profile_me(current_user: User = Depends(get_current_active_user),db:Session=Depends(get_db)):
    user = get_user_by_id(db=db,user_id=current_user.id)
    user_detail = get_user_detail_by_id(db,user_id=user.id)
    return Response(code="200", status="OK", message="Success Read User Detail",result=user_detail)

@router.patch("/profile/",dependencies=[Depends(validate_token)],tags=["Profile"])
async def update_profile_me(request:RequestUserDetailUpdate,current_user: User = Depends(get_current_active_user), db:Session = Depends(get_db)):
    user_updated = update_user_detail(user_detail=request.parameter,user_id=current_user.id,db=db)
    return Response(code="200",status="OK",message="Success Update User Detail",result=user_updated).dict(exclude_none=True)