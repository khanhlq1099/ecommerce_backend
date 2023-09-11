from sqlalchemy.orm import Session
from schemas.sub_category import  SubCategoryBase,SubCategoryUpdate
from models.sub_category import Product_Sub_Category
from models.category import Product_Category
from fastapi import HTTPException


## Sub Category
# Get sub cat by name or get all
def get_all_sub_category(db:Session, name:str, skip:int = 0, limit:int=100):
    if name is not None and len(name) > 0:
        relative_name = '%'+name+'%'
        cat = db.query(Product_Sub_Category)\
            .filter(Product_Sub_Category.name.like(relative_name))\
            .offset(skip).limit(limit).all()
        return cat
    return db.query(Product_Sub_Category).offset(skip).limit(limit).all()

# Get cat by id
def get_sub_category_by_id(db:Session, id:int):
    cat = db.query(Product_Sub_Category)\
            .filter(Product_Sub_Category.id == id).first()
    return cat

# Add
def add_sub_category(db:Session,sub_category:SubCategoryBase):
    check = db.query(Product_Category).filter(Product_Category.id == sub_category.product_category_id).first()
    if check is None:
        raise HTTPException(status_code=404, detail="Product Category not found!")
    
    check_name_sub_cat = db.query(Product_Sub_Category)\
                .filter(Product_Sub_Category.name == sub_category.name\
                        ,Product_Sub_Category.product_category_id==sub_category.product_category_id).first()

    if check_name_sub_cat:
        raise HTTPException(status_code=404, detail="Product Sub Category name already exists")
    
    sub_cat = Product_Sub_Category(**sub_category.dict())
    db.add(sub_cat)
    db.commit()
    db.refresh(sub_cat)
    return(True,sub_cat)

# Delete
def delete_sub_category_by_id(db:Session,id:str):
    cmd_del = db.query(Product_Sub_Category).filter(Product_Sub_Category.id == id).first()
    if not cmd_del:
        raise HTTPException(status_code=400, detail="Sub Category is non-existent")
    db.delete(cmd_del)
    db.commit()
    return(True)

# Update
def update_sub_category_by_id(db:Session,id:int, sub_category:SubCategoryUpdate):
    exists_sub_category = db.query(Product_Sub_Category).filter(Product_Sub_Category.id == id).first()
    if exists_sub_category is None:
        raise HTTPException(status_code=404, detail="Product Sub Category is not found!")
    
    check_name = db.query(Product_Sub_Category).filter(Product_Sub_Category.name == sub_category.name).first()
    if check_name:
        raise HTTPException(status_code=404, detail="Product Sub Category name already exists.")
    
    new_sub_category = sub_category.dict(exclude_unset=True)
    for key,value in new_sub_category.items():
        setattr(exists_sub_category,key,value)
    db.commit()
    db.refresh(exists_sub_category)
    return exists_sub_category