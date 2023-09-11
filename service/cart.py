from sqlalchemy.orm import Session,joinedload
from models.cart import Cart, Cart_Item
from schemas.cart import CartItemBase
from service.product import get_product_by_id
from fastapi import HTTPException
from models.product import Product

## Cart
# Get cart
def get_cart_by_user_id(db:Session, user_id:int, skip:int = 0, limit:int =100):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if cart is None:
        raise HTTPException(status_code=404,detail="Cart is non-exists.")
    return cart

def add_cart_by_user_id(db:Session,user_id:int):
    cart = Cart(user_id=user_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

## Cart Item
# Add
def add_cart_item(db:Session,user_id:int,cart_item:CartItemBase):
    cart = get_cart_by_user_id(db=db,user_id=user_id)
    if cart is None:
        cart = add_cart_by_user_id(db=db, user_id=user_id)

    # Check product exists
    product = get_product_by_id(db=db,id=cart_item.product_id)
    if product is None:
        raise HTTPException(status_code=404,detail="Product is non-existent")
    
    # if product.quantity < cart_item.quantity:
    #     raise HTTPException(status_code=400, detail="Product quantity is not enough")

    exists_cart_item = db.query(Cart_Item).filter(Cart_Item.product_id == cart_item.product_id,Cart_Item.cart_id == cart.id).first()
    if exists_cart_item is None:
        exists_cart_item = Cart_Item(cart_id=cart.id,**cart_item.dict(),amount=cart_item.quantity*product.price)
        db.add(exists_cart_item)
        db.commit()
        db.refresh(exists_cart_item)
        return exists_cart_item
    new_cart_item = cart_item.dict(exclude_unset=True)
    for key,value in new_cart_item.items():
        setattr(exists_cart_item,key,value)

    exists_cart_item.amount = exists_cart_item.quantity * product.price

    db.commit()
    db.refresh(exists_cart_item)

    return exists_cart_item

# Get
def get_cart_item(db:Session, user_id:int, skip:int = 0, limit:int =100):
    cart = get_cart_by_user_id(db=db, user_id=user_id)
    cart_item = db.query(Cart_Item).filter(Cart_Item.cart_id == cart.id)\
                .options(joinedload(Cart_Item.product))\
                .offset(skip).limit(limit=limit).all()

    return cart_item

# Delete
def delete_cart_item(db:Session, id:int):
    cart_item = db.query(Cart_Item).filter(Cart_Item.id == id).first()
    if cart_item is None:
        raise HTTPException(status_code=404, detail="Not found")
    # delete_cart_item = db.delete
    db.delete(cart_item)
    db.commit()
    return (True)