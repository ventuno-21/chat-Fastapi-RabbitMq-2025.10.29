from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("1"))


def hash_password(password: str) -> str:
    if isinstance(password, bytes):
        password = password.decode("utf-8")
    return pwd_context.hash(password[:72])


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain[:72], hashed)
