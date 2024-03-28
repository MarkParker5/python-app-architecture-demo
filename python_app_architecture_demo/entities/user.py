from pydantic import BaseModel

# default user representation
class User(BaseModel):
    name: str
    email: str

# used for creating a new user only
class UserCreate(User):
    name: str
    email: str
    password: str
