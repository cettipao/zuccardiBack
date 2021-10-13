from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    token: str

    class Config:
        orm_mode = True
