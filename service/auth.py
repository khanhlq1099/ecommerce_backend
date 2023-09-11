from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from service.user import get_user_by_id,get_user_by_email
from sqlalchemy.orm import Session
from datetime import timedelta,datetime
from jose import JWTError, jwt
from schemas.auth import TokenData
from utils.utils import get_db
from models.user import User
from pydantic import ValidationError

SECRET_KEY = "d289e9fa2539892d81458669ee6834cd87abaa40b9d543f4e17e7f7b0b567be8"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get email => return email
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        # print(datetime.fromtimestamp(payload.get('exp')))
        # print(datetime.now())
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(status_code=403, detail="Token expired")
        return payload.get('email')
    except(JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )

# Check password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Check login success
def authenticate_user(db:Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Email is not registered")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    return user 

# Generate Access Token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get user by token
async def get_current_user(db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:int = int(payload.get("sub"))       
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise HTTPException(status_code=403,detail="Please Login!")
    
    user = get_user_by_id(db=db, user_id=token_data.id)
    
    if user is None:
        raise credentials_exception
    return user

# Get user is activate
async def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_activate:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
