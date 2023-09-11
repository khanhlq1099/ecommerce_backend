from sqlalchemy.orm import Session
from service.user import get_user_detail_by_id
from models.order import Order,Order_Item
from schemas.order import OrderBase, OrderItemBase
from service.product import get_product_by_id
from service.cart import get_cart_item
from fastapi import HTTPException
from models.user import User_Detail
from models.payment import Payment_Method

## Order
# Get
def get_order_by_user_id(db:Session,user_id:int):
    return db.query(Order).filter(Order.user_id == user_id).first()

# Add
def add_order(db:Session,user_id:int):
    user_detail = get_user_detail_by_id(db=db,user_id=user_id)
    payment_method = db.query(Payment_Method).first()

    order = db.query(Order).filter(Order.user_id == user_detail.user_id).first()
    if order:
        return False
    order = Order(payment_method_id = payment_method.id)
    for col in Order.__table__.c:
        # if col.key not in ("id","payment_method_id","order_date","total_amount","status"):
        if col.key in User_Detail.__table__.c:
            setattr(order, col.key, getattr(user_detail, col.key))
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

# Update
def update_order_by_user_id(db:Session,user_id:int,order:OrderBase):
    exists_order = get_order_by_user_id(db=db,user_id=user_id)
    if exists_order is None:
        raise HTTPException(status_code=404, detail="Order not found!")
    new_order = order.dict(exclude_unset=True)
    for key,value in new_order.items():
        setattr(exists_order,key,value)
    db.commit()
    db.refresh(exists_order)
    
## Order_Item

def add_order_item(db:Session,user_id:int):
    order = get_order_by_user_id(db=db,user_id=user_id)
    if order is None:
        order = add_order(db=db,user_id=user_id)

    cart_items = get_cart_item(db=db,user_id=user_id)
    for cart_item in cart_items:
        # Check product exists
        product = get_product_by_id(db=db,id=cart_item.product_id)
        if product is None:
            raise HTTPException(status_code=404,detail="Product is non-existent")

    exists_order_item = db.query(Order_Item).filter(Order_Item.product_id == cart_item.product_id,Order_Item.order_id == order.id).first()
    if exists_order_item is None:
        exists_order_item = Order_Item(order_id = order.id)
        order_items = []
        for cart_item in cart_items:
            for col in Order_Item.__table__.c:
                if col.key not in ("id","order_id"):
                    setattr(exists_order_item, col.key, getattr(cart_item, col.key))

            order_item = Order_Item(product_id = exists_order_item.product_id,quantity = exists_order_item.quantity,\
                                    amount = exists_order_item.amount,order_id = order.id)
            order_items.append(order_item)

        update_order_by_user_id(db=db,user_id=user_id,order=OrderItemBase(total_amout = sum(order_item.amount)))

        # db.add_all(order_items)

        # db.commit()
        return order_items
    