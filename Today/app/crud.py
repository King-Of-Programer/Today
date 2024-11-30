from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List 
from . import models, schemas
from .models import Target
# CRUD Operations for Spy Cats

def create_spy_cat(db: Session, spy_cat: schemas.SpyCatCreate):
    db_spy_cat = models.SpyCat(**spy_cat.dict())
    db.add(db_spy_cat)
    try:
        db.commit()
        db.refresh(db_spy_cat)
    except IntegrityError:
        db.rollback()
        raise ValueError("Error: Duplicate breed or other integrity issue.")
    return db_spy_cat

def get_spy_cats(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.SpyCat).offset(skip).limit(limit).all()

def get_spy_cat(db: Session, spy_cat_id: int):
    return db.query(models.SpyCat).filter(models.SpyCat.id == spy_cat_id).first()

def update_spy_cat(db: Session, spy_cat_id: int, spy_cat_update: schemas.SpyCatBase):
    db_spy_cat = get_spy_cat(db, spy_cat_id)
    if not db_spy_cat:
        return None
    
    for key, value in spy_cat_update.dict(exclude_unset=True).items():
        setattr(db_spy_cat, key, value)
    
    db.commit()
    db.refresh(db_spy_cat)
    return db_spy_cat

def delete_spy_cat(db: Session, spy_cat_id: int):
    db_spy_cat = get_spy_cat(db, spy_cat_id)
    if not db_spy_cat:
        return False
    
    db.delete(db_spy_cat)
    db.commit()
    return True



def create_mission(db: Session, mission: schemas.MissionCreate):
    db_mission = models.Mission(cat_id=mission.cat_id)

    for target in mission.targets:
        db_target = models.Target(**target.dict(), mission=db_mission)
        db_mission.targets.append(db_target)

    db.add(db_mission)
    try:
        db.commit()
        db.refresh(db_mission)
    except IntegrityError:
        db.rollback()
        raise ValueError("Error: Unable to create mission due to integrity issue.")
    
    return db_mission

def get_missions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Mission).offset(skip).limit(limit).all()

def get_mission(db: Session, mission_id: int):
    return db.query(models.Mission).filter(models.Mission.id == mission_id).first()

