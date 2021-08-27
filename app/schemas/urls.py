from pydantic import BaseModel, validator
from datetime import datetime
import validators


class UrlBase(BaseModel):
    hash: str
    original_url: str
    creation_date: datetime
    expiration_date: datetime


class UrlStats(UrlBase):
    visits_count: int


class CreateUrl(BaseModel):
    original_url: str

    @validator('original_url')
    def validate_url(cls, val):
        if not validators.url(val):
            raise ValueError('URL is invalid.')
        if len(val) > 512:
            raise ValueError('URL is too long.')
        return val


class ListUrl(BaseModel):
    urls: list[UrlBase]


class ListUrlStats(BaseModel):
    urls: list[UrlStats]
