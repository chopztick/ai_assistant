from pydantic import BaseModel, EmailStr

class UserUpdate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
