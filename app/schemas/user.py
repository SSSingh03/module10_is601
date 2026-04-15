from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    email: str
    username: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)