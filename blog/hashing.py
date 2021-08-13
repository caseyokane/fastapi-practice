from passlib.context import CryptContext

# Context used to hash values 
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str): 
        return pwd_cxt.hash(password)