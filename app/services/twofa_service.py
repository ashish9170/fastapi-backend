
# services/twofa.py
import random
import string
from app.core.config import settings

# Access Redis client
redis_client = settings.redis_client  # Rename to redis_client for clarity

OTP_EXPIRY_SECONDS = 300  # 5 minutes

def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))

def save_otp(email: str, code: str):
    redis_client.setex(f"otp:{email}", OTP_EXPIRY_SECONDS, code)

def verify_otp(email: str, code: str) -> bool:
    stored = redis_client.get(f"otp:{email}")
    if stored and stored == code:
        redis_client.delete(f"otp:{email}")
        return True
    return False
