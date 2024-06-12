from pydantic import BaseModel
from typing import Optional


class StudentUpdateSchema(BaseModel):
    groups: Optional[str]
    institution: Optional[str]


class PartnerUpdateSchema(BaseModel):
    organization: Optional[str]
    position: Optional[str]


class UserUpdateSchema(BaseModel):
    fio: Optional[str]
    avatar_url: Optional[str]
    login: Optional[str]
    email: Optional[str]
    password: Optional[str]
    student_info: Optional[StudentUpdateSchema]
    partner_info: Optional[PartnerUpdateSchema]
