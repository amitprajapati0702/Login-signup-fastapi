import random
from datetime import datetime, timedelta
from app.config import OTP_EXPIRY_MINUTES  # We'll add this to config

def generate_otp(length: int = 6) -> str:
    """Generate a random OTP"""
    return "".join([str(random.randint(0, 9)) for _ in range(length)])

def get_otp_expiry():
    """Get OTP expiry time (current time + OTP_EXPIRY_MINUTES)"""
    return datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)

def is_otp_expired(otp_expiry: datetime) -> bool:
    """Check if OTP is expired"""
    return datetime.utcnow() > otp_expiry

def create_otp_email_body(otp: str) -> str:
    """Create HTML email body for OTP"""
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2>Email Verification</h2>
                <p>Your OTP for email verification is:</p>
                <div style="background-color: #f0f0f0; padding: 20px; text-align: center; margin: 20px 0; border-radius: 5px;">
                    <h1 style="color: #333; letter-spacing: 5px; margin: 0;">{otp}</h1>
                </div>
                <p>This OTP will expire in 10 minutes.</p>
                <p>If you didn't request this, please ignore this email.</p>
            </div>
        </body>
    </html>
    """