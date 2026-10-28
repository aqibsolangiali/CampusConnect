from pydantic import BaseModel, EmailStr, Field, ConfigDict

class Registration(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class Login(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr

class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    title: str
    department: str
    credits: int
    capacity: int
    instructor: str
    schedule: str
    description: str
    enrolled: int = 0

class OpportunityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    organization: str
    kind: str
    location: str
    description: str
    url: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
