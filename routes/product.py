from fastapi import APIRouter,Depends, HTTPException
from utils.utils import get_db
from service.auth import validate_token
from schemas.product import RequestProduct,Response,RequestProductUpdate
from sqlalchemy.orm import Session
import service.product as pd

router = APIRouter(
    prefix="/product",
    tags=["Product"],
    responses={404: {"description": "Not found"}},
)

# Router Product
@router.post("/",dependencies=[Depends(validate_token)])
async def create_product(request:RequestProduct,db:Session = Depends(get_db)):
    status,product = pd.add_product(db=db,product=request.parameter)
    if status:
        return Response(code="200",status="OK",message="Success Add Product",result=product).dict(exclude_none=True)
    return Response(code="400",status="Failure",message=product)

@router.get("/",dependencies=[Depends(validate_token)])
async def read_products(name:str | None = None,skip: int = 0,limit:int = 100,db:Session = Depends(get_db)):
    product = pd.get_all_products(db=db,name=name,skip=skip,limit=limit)
    if not product:
        raise HTTPException(status_code=404,detail="Product is non-existent")
    return Response(code="200", status="OK", message="Success Read Product",result=product)

@router.get("/{id}",dependencies=[Depends(validate_token)])
async def read_product_by_id(id:int,db:Session = Depends(get_db)):
    product = pd.get_product_by_id(db=db,id=id)
    if not product:
        raise HTTPException(status_code=404,detail="Product is non-existent")
    return Response(code="200", status="OK", message="Success Read Product",result=product)

@router.patch("/{id}",dependencies=[Depends(validate_token)])
async def update_product_by_id(request:RequestProductUpdate,id:int,db:Session = Depends(get_db)):
    updated_product = pd.update_product_by_id(db=db,id=id,product=request.parameter)
    return Response(code="200",status="OK",message="Success Update Sub Category",result=updated_product).dict(exclude_none=True)

@router.delete("/{id}",dependencies=[Depends(validate_token)])
async def detele_product(id:int, db:Session = Depends(get_db)):
    status = pd.delete_product_by_id(db=db,id=id)
    if not status:
        return {"detail":"Delete failed!"}
    return Response(code=200, status="OK",message="Deleted!")