from passlib.context import CryptContext

class HasherClass:
    def __init__(self):
        self.PasswordHasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.TokenGenerator = CryptContext(schemes=["des_crypt"], deprecated="auto")

    def HashOfPassword(self, Password: str) -> str:
        return self.PasswordHasher.hash(Password) #type: ignore

    def CheckPassword(self, Hash: str, Password: str) -> bool:
        return self.PasswordHasher.verify(Password, Hash) #type: ignore

    
    def GetToken(self, Login: str, HashOfPassword: str) -> str:
        return self.TokenGenerator.hash(Login + HashOfPassword) #type: ignore

    def CheckToken(self, Token: str, Login: str, HashOfPassword: str) -> bool:
        return self.TokenGenerator.verify(Token, Login + HashOfPassword) #type: ignore