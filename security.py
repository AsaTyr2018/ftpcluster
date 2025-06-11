import os
from cryptography.fernet import Fernet
from itsdangerous import URLSafeTimedSerializer, BadSignature

SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme')
FERNET_KEY = os.environ.get('FERNET_KEY')
if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key()
    os.environ['FERNET_KEY'] = FERNET_KEY.decode()

fernet = Fernet(FERNET_KEY)
serializer = URLSafeTimedSerializer(SECRET_KEY)

def encrypt_value(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt_value(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

def sign_username(username: str) -> str:
    return serializer.dumps(username)

def verify_username(token: str, max_age: int = 3600) -> str | None:
    if not token:
        return None
    try:
        return serializer.loads(token, max_age=max_age)
    except BadSignature:
        return None
