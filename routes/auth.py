from fastapi import APIRouter,Depends, HTTPException, status
from service.auth import authenticate_user, create_access_token,get_current_active_user,validate_token
from schemas.auth import LoginInput,EmailSchema
from sqlalchemy.orm import Session
from utils.utils import get_db
from datetime import timedelta
# from schemas.user import User
from models.user import User
from schemas.user import UserOut
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

ACCESS_TOKEN_EXPIRE_MINUTES = 12000

conf = ConnectionConfig(MAIL_USERNAME = 'khanhlq1099.1@gmail.com',
                        MAIL_PASSWORD = 'eukiqxpsomgkusue',
                        MAIL_FROM = 'khanhlq1099.1@gmail.com',
                        MAIL_PORT = 587,
                        MAIL_SERVER = 'smtp.gmail.com',
                        MAIL_FROM_NAME='Application',
                        MAIL_STARTTLS = True,
                        MAIL_SSL_TLS = False,
                        USE_CREDENTIALS = True,
                        VALIDATE_CERTS = True
                        )


router = APIRouter(
    # prefix="/user",
    tags=['Authentication'],
    # responses={404: {"description": "Not found"}},
)

# Enter user and pw then generate access token
@router.post("/login/")
async def login_for_access_token(login_input: LoginInput,db:Session = Depends(get_db)):
    user = authenticate_user(db, login_input.email, login_input.password)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"Status" :"Success", "Access_token": access_token, "Token_type": "Bearer"}

# Get current user by token
@router.get("/user/me/",dependencies=[Depends(validate_token)])
async def read_current_user(current_user: User = Depends(get_current_active_user)):
    return UserOut(**current_user.__dict__)

# Verify Email
@router.post("/email/",dependencies=[Depends(validate_token)])
async def verify_email(email: EmailSchema):
    html = """ 
    <html>
    <body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
    <div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
    <div style="margin: 0 auto; width: 90%; text-align: center;">
        <!-- <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">{{ body.title }}</h1> -->
        <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center;">
        <h3 style="margin-bottom: 30px; font-size: 24px;">Verify your email</h3>
        <p style="margin-bottom: 50px;">Hi, click the link below to verify your email and start enjoy app.</p>
        <a style="display: block; margin: 0 auto; border: none; background-color: 	rgb(30,144,255); color: white; width: 150px; line-height: 24px; padding: 10px; font-size: 24px; border-radius: 10px; cursor: pointer; text-decoration: none;"
            # href="http://127.0.0.1:8000/user/me/"
            target="_blank"
        >
            Verify Email
        </a>
        </div>
    </div>
    </div>
    </body>
    </html>
    """
    message = MessageSchema(
        subject="Email Verification",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "Email has been sent"})