from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.constants import NAME_MAX_LENGTH, STR_MIN_LENGTH


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=NAME_MAX_LENGTH)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = STR_MIN_LENGTH
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=NAME_MAX_LENGTH)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @validator('name', 'description', 'full_amount', pre=True)
    def null_not_allowed(cls, value):
        if value is None:
            raise ValueError('Поле не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
