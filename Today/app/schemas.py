from pydantic import BaseModel
from typing import List, Optional

class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None

class TargetCreate(TargetBase):
    pass

class Target(TargetBase):
    id: int
    complete: bool

    class Config:
        orm_mode = True

class MissionBase(BaseModel):
    cat_id: int

class MissionCreate(MissionBase):
    targets: List[TargetCreate]

class Mission(MissionBase):
    id: int
    complete: bool
    targets: List[Target] = []

    class Config:
        orm_mode = True

class SpyCatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float

class SpyCatCreate(SpyCatBase):
    pass

class SpyCat(SpyCatBase):
    id: int

    class Config:
        orm_mode = True