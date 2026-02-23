from pydantic import BaseModel, Field
from typing import Optional

class StudentModel(BaseModel):
    roll_number: str
    password_hash: str
    is_eligible: bool = True
    has_voted: bool = False

class StudentResponse(BaseModel):
    roll_number: str
    is_eligible: bool
    has_voted: bool
    
    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    roll_number: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    roll_number: Optional[str] = None
    
class VoteSubmit(BaseModel):
    candidate_id: str
