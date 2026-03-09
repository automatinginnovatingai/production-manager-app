import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, stored_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), stored_hash.encode())

def hash_pin(pin: str) -> str:
    return bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()

def verify_pin(pin: str, stored_hash: str) -> bool:
    return bcrypt.checkpw(pin.encode(), stored_hash.encode())


