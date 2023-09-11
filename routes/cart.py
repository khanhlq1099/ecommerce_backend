from fastapi import APIRouter,Depends, HTTPException
from utils.utils import get_db
from service.auth import validate_token,get_current_active_user
from schemas.cart import RequestCartItem,Response,CartItemOut
from sqlalchemy.orm import Session
import service.cart as cart
from models.user import User
from service.user import get_user_by_email

router = APIRouter(
    prefix="/cart_item",
    tags=["Cart"],
    responses={404: {"description": "Not found"}},
)

@router.post("/",dependencies=[Depends(validate_token)])
async def create_or_update_cart_item(request:RequestCartItem,\
                            current_user: User = Depends(get_current_active_user),\
                            db:Session = Depends(get_db)):
    cart_item = cart.add_cart_item(db=db,user_id=current_user.id,\
                                   cart_item=request.parameter)
    return Response(code="200",status="OK",message="Success Add Product",result=cart_item).dict(exclude_none=True)

@router.get("/",dependencies=[Depends(validate_token)])
async def read_cart_item(current_user: User = Depends(get_current_active_user),\
                            db:Session = Depends(get_db)):
    cart_item = cart.get_cart_item(db=db,user_id=current_user.id)
    cart_item_out = [CartItemOut.from_orm(x) for x in cart_item]
    return Response(code="200",status="OK",message="Success Get Item in Cart",result=cart_item_out)

@router.delete("/{id}",dependencies=[Depends(validate_token)])
async def delete_cart_item(id:int, db:Session = Depends(get_db)):
    status = cart.delete_cart_item(db=db,id=id)
    if not status:
        return {"detail":"Delete failed!"}
    return Response(code=200, status="OK",message="Deleted!")