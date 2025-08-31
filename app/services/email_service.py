#services/email.py
import httpx
from app.core.config import settings

def send_2fa_email(email: str, code: str):
    payload = {
        "sender": {"name": "MyApp", "email": "ashishvishwakarma55521@gmail.com"},
        "to": [{"email": email}],
        "subject": "Your 2FA Code",
        "htmlContent": f"<p>Your code is: <strong>{code}</strong></p>"
    }

    headers = {
        "api-key": settings.BRAVO_API_KEY,
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    try:
        response = httpx.post(settings.BRAVO_API_URL, json=payload, headers=headers)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print("Email send failed:", e)
