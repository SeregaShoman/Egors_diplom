from typing import Optional
from pydantic import BaseModel, Field, model_validator, validator


class SignUpBody(BaseModel):
    fio: str = Field(description="Имя Фамили Отчество")
    avatar_url: str = Field(description="http://url/image")
    login: str = Field(description="1114")
    email: str = Field(description="user@mail.ru")
    password: str = Field(description="some_pass")
    role: str = Field(description="Студент")
    group: Optional[str] = Field(None, description="ИСП-3")
    institution: Optional[str] = Field(None, description="Самарский Гос Университет")
    organization: Optional[str] = Field(None, description="ООО Кореельский")
    position: Optional[str] = Field(None, description="Исполнительный директор")

    @validator('role')
    def role_must_be_student_or_partner(cls, v):
        if v not in {'Студент', 'Партнёр', 'Админ'}:
            raise ValueError('role must be either Студент or Партнёр')
        return v

    @model_validator(mode='after')
    def check_role_constraints(cls, values):
        role = values.role
        group = values.group
        institution = values.institution
        organization = values.organization
        position = values.position

        if role == 'Студент':
            if not group or not institution:
                raise ValueError('group and institution must be provided if role is Студент')
            if organization or position:
                raise ValueError('organization and position must not be provided if role is Студент')
        
        if role == 'Партнёр':
            if not organization or not position:
                raise ValueError('organization and position must be provided if role is Партнёр')
            if group or institution:
                raise ValueError('group and institution must not be provided if role is Партнёр')
            
        if role == 'Админ':
            if group or institution or organization or position:
                raise ValueError("group and institution and organization and position must not be provided if role is Админ")

        return values


class SignInBody(BaseModel):
    login: str = Field(description="1114")
    password: str = Field(description="some_pass")