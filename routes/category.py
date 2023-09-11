from fastapi import APIRouter,Depends, HTTPException
from utils.utils import get_db
from service.auth import validate_token
from schemas.category import RequestCategory,Response,CategoryBase,RequestCategoryUpdate
from sqlalchemy.orm import Session
import service.category as cat 

router = APIRouter(
    prefix="/category",
    tags=["Category"],
    responses={404: {"description": "Not found"}},
)

# Router Category
@router.post("/",dependencies=[Depends(validate_token)])
async def create_product_category(request:RequestCategory,db:Session = Depends(get_db)):
    status,cate = cat.add_category(db=db,category=request.parameter)
    cate_out = CategoryBase(**cate.__dict__)
    if not status:
        raise HTTPException(status_code=400,detail="Failure")
    return Response(code="200",status="OK",message="Success Add Category",result=cate_out).dict(exclude_none=True)

@router.get("/",dependencies=[Depends(validate_token)])
async def read_product_categories(name:str | None = None ,skip: int = 0,limit:int = 100, db:Session=Depends(get_db)):
    categories = cat.get_categories(db=db,name=name,skip=skip,limit=limit)
    if not categories:
        raise HTTPException(status_code=404,detail="Category is non-existent")
    return Response(code="200",status="OK",message="Success get Product Categories.",result=categories)

@router.get("/{id}",dependencies=[Depends(validate_token)])
async def read_product_category_id(id:int,db:Session = Depends(get_db)):
    cate = cat.get_category_by_id(db=db,id=id)
    if not cate:
        raise HTTPException(status_code=404,detail="Category is non-existent")
    else:
        return Response(code="200", status="OK", message="Success Read Category",result=cate)

@router.patch("/{id}",dependencies=[Depends(validate_token)])
async def update_product_category(request:RequestCategoryUpdate,id:int,db:Session = Depends(get_db)):
    category_updated = cat.update_category_by_id(db=db,id=id,category=request.parameter)
    return Response(code="200",status="OK",message="Success Update Category",result=category_updated).dict(exclude_none=True)

@router.delete("/{id}",dependencies=[Depends(validate_token)])
async def detele_product_category(id:str, db:Session = Depends(get_db)):
    status = cat.delete_category_by_id(db=db,id=id)
    if status:
        return Response(code=200, status=status,message="Deleted!")
    else: return {"detail":"Delete failed!"}
