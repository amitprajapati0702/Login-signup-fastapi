from pydantic import BaseModel,EmailStr


class LoginRequest(BaseModel):
    email : EmailStr
    password:str
    captcha_id :str
    captcha_answer : int

    