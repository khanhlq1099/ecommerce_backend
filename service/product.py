from sqlalchemy.orm import Session
from schemas.product import ProductBase,ProductUpdate
from models.product import Product
from fastapi import HTTPException
from models.sub_category import Product_Sub_Category

## Product
# Get product by name or get all
def get_all_products(db:Session, name:str, skip:int = 0, limit:int=100):
    if name is not None and len(name) > 0:
        relative_name = '%'+name+'%'
        product = db.query(Product)\
                .filter(Product.name.like(relative_name))\
                .offset(skip).limit(limit).all()
        return product
    return db.query(Product).offset(skip).limit(limit).all()

# Get cat by id
def get_product_by_id(db:Session, id:int):
    product = db.query(Product)\
            .filter(Product.id == id).first()
    return product

# Add
def add_product(db:Session,product:ProductBase): 
    check = db.query(Product_Sub_Category).filter(Product_Sub_Category.id == product.product_sub_category_id).first()
    if check is None:
        raise HTTPException(status_code=404, detail="Product Category not found!")
    
    check_product = db.query(Product)\
                    .filter(Product.name == product.name\
                            , Product.product_sub_category_id == product.product_sub_category_id).first()
    if check_product:
        raise HTTPException(status_code=404, detail="Product name already exists.")

    product = Product(**product.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return(True,product)

# Delete
def delete_product_by_id(db:Session,id:str):
    cmd_del = db.query(Product).filter(Product.id == id).first()
    if not cmd_del:
        raise HTTPException(status_code=400, detail="Product is non-existent")
    db.delete(cmd_del)
    db.commit()
    return(True)

# Update
def update_product_by_id(db:Session,id:int, product:ProductUpdate):
    exists_product = db.query(Product).filter(Product.id == id).first()
    if exists_product is None:
        raise HTTPException(status_code=404, detail="Product is not found!")
    
    check_name = db.query(Product).filter(Product.name == product.name).first()
    if check_name:
        raise HTTPException(status_code=404, detail="Product name already exists.")
    
    new_product = product.dict(exclude_unset=True)
    for key,value in new_product.items():
        setattr(exists_product,key,value)
    db.commit()
    db.refresh(exists_product)
    return exists_product