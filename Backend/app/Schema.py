from pydantic import BaseModel,EmailStr


class LoginRequest(BaseModel):
    email : EmailStr
    password:str
    captcha_id :str
    captcha_answer : int

class MailBody(BaseModel):
    to: list[EmailStr]
    subject: str
    body: str

class SendOTPRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str