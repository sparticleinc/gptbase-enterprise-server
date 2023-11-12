from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class EnvironmentDataOut(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    sort: Optional[int] = None
    data: Optional[List[str]] = None

    class Config:
        orm_mode = True


class EnvironmentDataIn(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    sort: Optional[int] = None
    data: Optional[List[str]] = None

    class Config:
        orm_mode = True
