from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., examples=["camila"])
    email: str  = Field(..., max_length=120, min_length=5, examples=["nico123"])
    edad: int | None = None
    username: str = Field(..., max_length=120, min_length=5, examples=["nico123"])


class UserDb(User):
    # id: str | None = Field(alias="_id")
    password: str = Field(..., description="password hashed")


class UserOut(User):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True