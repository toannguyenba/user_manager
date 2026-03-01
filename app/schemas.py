
from pydantic import BaseModel, EmailStr, Field, validator, field_validator
import re

import re
from pydantic import BaseModel, Field, validator

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    firstname: str = Field(..., min_length=1, max_length=50)
    lastname: str = Field(..., min_length=1, max_length=50)
    zip_code: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        # Không được có khoảng trắng
        if " " in v:
            raise ValueError("Email must not contain spaces")

        # Phải có đúng 1 ký tự @
        if v.count("@") != 1:
            raise ValueError("Email must contain exactly one '@'")

        local_part, domain_part = v.split("@")

        # Local part không được rỗng
        if not local_part:
            raise ValueError("Email local part is required")

        # Domain phải chứa dấu chấm
        if "." not in domain_part:
            raise ValueError("Email domain must contain '.'")

        # Không được bắt đầu/kết thúc bằng dấu chấm
        if domain_part.startswith(".") or domain_part.endswith("."):
            raise ValueError("Invalid domain format")

        # Regex đơn giản
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")

        return v

    @field_validator("zip_code")
    @classmethod
    def validate_zip(cls, v):
        if not re.match(r"^[0-9]{5,6}$", v):
            raise ValueError("zip_code must be 5-6 digits")
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    zip_code: str | None = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
