from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    email: str
    full_name: str

    class Config:
        orm_mode = True
