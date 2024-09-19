from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
        str_strip_whitespace = True