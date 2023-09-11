from fastapi import APIRouter,Depends, HTTPException
from utils.utils import get_db
from service.auth import validate_token
from schemas.sub_category import RequestSubCategory,Response,RequestSubCategoryUpdate
from sqlalchemy.orm import Session
import service.sub_category as sc

router = APIRouter(
    prefix="/sub_category",
    tags=["Sub Category"],
    responses={404: {"description": "Not found"}},
)

# Router Sub Category
@router.post("/",dependencies=[Depends(validate_token)])
async def create_product_sub_category(request:RequestSubCategory,db:Session = Depends(get_db)):
    status,sub_cat = sc.add_sub_category(db=db,sub_category=request.parameter)
    if status:
        return Response(code="200",status="OK",message="Success Add Sub Category",result=sub_cat).dict(exclude_none=True)
    return Response(code="400",status="Failure",message=sub_cat)
 
@router.get("/",dependencies=[Depends(validate_token)],tags=["Sub Category"])
async def read_product_sub_categories(name:str | None = None,skip: int = 0,limit:int = 100,db:Session = Depends(get_db)):
    sub_cat = sc.get_all_sub_category(db=db,name=name,skip=skip,limit=limit)
    if not sub_cat:
        raise HTTPException(status_code=404,detail="Sub Category is non-existent")
    return Response(code="200", status="OK", message="Success Read Sub Category",result=sub_cat)

@router.get("/{id}",dependencies=[Depends(validate_token)])
async def read_product_category_id(id:int,db:Session = Depends(get_db)):
    sub_cate = sc.get_sub_category_by_id(db=db,id=id)
    if not sub_cate:
        raise HTTPException(status_code=404,detail="Sub Category is non-existent")
    return Response(code="200", status="OK", message="Success Read Sub Category",result=sub_cate)

@router.patch("/{id}",dependencies=[Depends(validate_token)])
async def update_product_sub_category(request:RequestSubCategoryUpdate,id:int,db:Session = Depends(get_db)):
    sub_category_updated = sc.update_sub_category_by_id(db=db,id=id,sub_category=request.parameter)
    return Response(code="200",status="OK",message="Success Update Sub Category",result=sub_category_updated).dict(exclude_none=True)

@router.delete("/",dependencies=[Depends(validate_token)],tags=["Sub Category"])
async def detele_product_sub_category(id:str, db:Session = Depends(get_db)):
    status = sc.delete_sub_category_by_id(db=db,id=id)
    if status:
        return Response(code=200, status="OK",message="Deleted!")
    return {"detail":"Delete failed!"}
