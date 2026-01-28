import random
import uuid

captcha_store = {}

def generate_captcha():
    a = random.randint(1,9)
    b = random.randint(1,9)
    captcha_id = str(uuid.uuid4())
    answer = a+b
    captcha_store[captcha_id] = answer

    # database

    return{
        "captcha_id": captcha_id,
        "question": { b:{a} , a:{b} },
    }

def verify_captcha(captcha_id : str , user_answer:int):
    correct = captcha_store.get(captcha_id)
    if correct is None:
        return False
    

    del captcha_store[captcha_id]

    return correct == user_answer