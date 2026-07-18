from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    mobile_number: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: str
    
    class Config:
        from_attributes = True

class UserSettingsUpdate(BaseModel):
    morning_broadcast_hour: Optional[int] = None
    noon_broadcast_hour: Optional[int] = None
    evening_broadcast_hour: Optional[int] = None