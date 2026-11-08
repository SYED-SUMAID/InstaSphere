from pydantic import BaseModel, EmailStr, Field


# User registration
class UserCreate(BaseModel):

    name: str = Field(min_length=2, max_length=255)

    username: str = Field(min_length=3, max_length=100)

    email: EmailStr

    password: str = Field(min_length=8)


# User login
class UserLogin(BaseModel):

    email: EmailStr

    password: str


# User response
class UserRead(BaseModel):

    id: int

    name: str

    username: str

    email: EmailStr

    bio: str | None = None

    profile_picture: str | None = None