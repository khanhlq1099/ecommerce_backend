from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from routes.user import router as user
from routes.auth import router as auth
from routes.product import router as product
from routes.category import router as category
from routes.sub_category import router as sub_category
from routes.cart import router as cart
from routes.order import router as order
import uvicorn

app = FastAPI(
    title="E-commerce API",
    description="E-commerce API created with FastAPI and JWT Authenticated"
)

app.include_router(auth)
app.include_router(user)
app.include_router(category)
app.include_router(sub_category)
app.include_router(product)
app.include_router(cart)
app.include_router(order)

# if __name__ == '__main__':
#     uvicorn.run('main:app', reload=True)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNjg3NDcxMDIwfQ.Ulouu3qHY9iYvA4wf19ZZmA36SghywpgyeUMGprsY-o