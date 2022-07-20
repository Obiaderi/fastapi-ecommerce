from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def hash_password(password):
        return pwd_context.hash(password)

    def verify(request_password, hashed_password):
        return pwd_context.verify(request_password, hashed_password)
