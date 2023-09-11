from sqlalchemy.orm import Session
from schemas.category import CategoryBase,CategoryUpdate
from models.category import Product_Category
from fastapi import HTTPException

## Category

# Get all category
def get_categories(db:Session,name:str,skip:int = 0, limit:int=100):
    if name is not None and len(name) > 0:
        relative_name = '%'+name+'%'
        cat = db.query(Product_Category)\
            .filter(Product_Category.name.like(relative_name))\
            .offset(skip).limit(limit).all()
        return cat
    return db.query(Product_Category).offset(skip).limit(limit).all()

# Get cat by id
def get_category_by_id(db:Session, id:int):
    cat = db.query(Product_Category)\
            .filter(Product_Category.id == id).first()
    return cat

# Add
def add_category(db:Session, category:CategoryBase):
    check_category = db.query(Product_Category)\
                    .filter(Product_Category.name == category.name).first()
    
    if check_category:
        raise HTTPException(status_code=404, detail="Category already exists.")

    cat = Product_Category(**category.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return(True,cat)

# Delete
def delete_category_by_id(db:Session,id:str):
    cmd_del = db.query(Product_Category).filter(Product_Category.id == id).first()
    if not cmd_del:
        raise HTTPException(status_code=400, detail="Category is non-existent")
    db.delete(cmd_del)
    db.commit()
    return(True)

# Update
def update_category_by_id(db:Session,id:int, category:CategoryUpdate):
    exists_category = db.query(Product_Category).filter(Product_Category.id == id).first()
    if exists_category is None:
        raise HTTPException(status_code=404, detail="Product Category is not found!")
    
    check_name = db.query(Product_Category).filter(Product_Category.name == category.name).first()
    if check_name:
        raise HTTPException(status_code=404, detail="Product Category name already exists.")
    
    new_category = category.dict(exclude_unset=True)
    for key,value in new_category.items():
        setattr(exists_category,key,value)
    db.commit()
    db.refresh(exists_category)
    return exists_category
