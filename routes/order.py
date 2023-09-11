from fastapi import APIRouter,Depends, HTTPException
from service.auth import validate_token,get_current_active_user
from schemas.order import OrderBase,Response,RequestOrder,RequestOrderItem
from models.user import User
from sqlalchemy.orm import Session
from utils.utils import get_db
from service.order import add_order,update_order_by_user_id,add_order_item

router = APIRouter(
    tags=["Order"],
    responses={404: {"description": "Not found"}},
)

@router.post("/order",dependencies=[Depends(validate_token)])
async def create_order(current_user: User = Depends(get_current_active_user),\
                                 db:Session = Depends(get_db)):
    # user_detail = get_user_detail_by_id(db=db,user_id=current_user.id)
    # print(user_detail)
    order = add_order(db=db,user_id=current_user.id)
    return Response(code="200",status="OK",message="Success Add Order",result=order).dict(exclude_none=True)

@router.patch("/order",dependencies=[Depends(validate_token)])
async def update_order(request:RequestOrder,current_user: User = Depends(get_current_active_user),\
                                 db:Session = Depends(get_db)):
    order_update = update_order_by_user_id(db=db,user_id=current_user.id,order=request.parameter)
    return Response(code="200",status="OK",message="Success Update Order",result=order_update).dict(exclude_none=True)

@router.post("/order_item",dependencies=[Depends(validate_token)])
async def create_order_item(current_user: User = Depends(get_current_active_user),\
                            db:Session = Depends(get_db)):
    order_item = add_order_item(db=db,user_id=current_user.id)
    return Response(code="200",status="OK",message="Success Add Order Item",result=order_item).dict(exclude_none=True)
