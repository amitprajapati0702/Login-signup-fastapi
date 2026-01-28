from fastapi import APIRouter,Depends,HTTPException
from app.Database import Base, get_db,engine
from sqlalchemy.orm import Session
from app.model import User
from app.Schema import LoginRequest
from app.utils.captcha import generate_captcha,verify_captcha
router = APIRouter()

Base.metadata.create_all(bind=engine)


@router.get("/")
def greeting():
    return {"Message":"Hello,FastAPI is Working !"}

# Show all the users information
@router.get("/users")
def get_users(db:Session = Depends(get_db)):
    users = db.query(User).all()
    return users

#show only particular user information
@router.get("/users/{id}")
def get_user(id:int , db:Session=Depends(get_db)):
    oneuser = db.query(User).filter(User.id == id).first()
    return oneuser

# Create a new user
@router.post("/users")
def create_user():
    return {"Message":"User baki he"}


# Captcha API 
@router.get("/captcha")
def get_captcha():
     return generate_captcha()


# Vlidate a captcha id
# Login User
@router.post("/users/login")
def login_user(data : LoginRequest , db:Session = Depends(get_db)):
    is_valid_captcha = verify_captcha(data.captcha_id , data.captcha_answer)
    if not is_valid_captcha:
        raise HTTPException(status_code=400,detail="Invalid Captcha")
    
    user = db.query(User).filter(User.email == data.email).first()
    if not user or user.password != data.password: # type: ignore
        raise HTTPException(status_code=400,detail="Invalid Email or Password")
    
    
    return {"Message":"Login Successful"}
    



   