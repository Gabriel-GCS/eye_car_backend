from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthUtil:
    def password_encrypt(self, password):
        return pwd_context.hash(password)

    def check_password(self, password, password_encrypted):
        return pwd_context.verify(password, password_encrypted)