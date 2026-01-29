from app.utils.otp import create_otp_email_body, generate_otp, get_otp_expiry, is_otp_expired
from fastapi import APIRouter,Depends,HTTPException # type: ignore
from app.Database import Base, get_db,engine
from sqlalchemy.orm import Session
from app.model import User
from app.Schema import LoginRequest, MailBody, SendOTPRequest, VerifyOTPRequest
from app.mailer import send_email
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


### EMAIL SENDING ROUTE ###
@router.post("/send-email")
def email_send(data:MailBody):
    is_sent = send_email(data.model_dump())
    if not is_sent:
        raise HTTPException(status_code=500,detail="Email sending failed")
    return {"Message":"Email sent successfully"}  

### OTP Sending Route ###  
@router.post("/send-otp")
def send_otp(data: SendOTPRequest, db: Session = Depends(get_db)):
    """Send OTP to email"""
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate OTP
    otp = generate_otp()
    otp_expiry = get_otp_expiry()
    
    # Save OTP to database
    user.otp = otp # pyright: ignore[reportAttributeAccessIssue]
    user.otp_expiry = otp_expiry # pyright: ignore[reportAttributeAccessIssue]
    db.commit()
    
    # Send OTP via email
    email_body = create_otp_email_body(otp)
    is_sent = send_email({
        "to": [data.email],
        "subject": "Your OTP for Email Verification",
        "body": email_body
    })
    
    if not is_sent:
        raise HTTPException(status_code=500, detail="Failed to send OTP")
    
    return {"Message": "OTP sent successfully to your email"}


### OTP Verification ROute ####
@router.post("/verify-otp")
def verify_otp(data: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verify OTP"""
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.otp: # type: ignore
        raise HTTPException(status_code=400, detail="No OTP requested")
    
    if is_otp_expired(user.otp_expiry): # type: ignore
        raise HTTPException(status_code=400, detail="OTP expired")
    
    if user.otp != data.otp: # type: ignore
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Mark user as verified
    user.is_verified = 1 # type: ignore
    user.otp = None # type: ignore
    user.otp_expiry = None # type: ignore
    db.commit()
    
    return {"Message": "Email verified successfully"}




   