from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, database

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/spy_cats/", response_model=schemas.SpyCat)
def create_spy_cat(spy_cat: schemas.SpyCatCreate, db: Session = Depends(get_db)):
    return crud.create_spy_cat(db=db, spy_cat=spy_cat)

@router.get("/spy_cats/", response_model=List[schemas.SpyCat])
def read_spy_cats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_spy_cats(db=db, skip=skip, limit=limit)

@router.get("/spy_cats/{spy_cat_id}", response_model=schemas.SpyCat)
def read_spy_cat(spy_cat_id: int, db: Session = Depends(get_db)):
    db_spy_cat = crud.get_spy_cat(db=db, spy_cat_id=spy_cat_id)
    
    if not db_spy_cat:
        raise HTTPException(status_code=404, detail="Spy Cat not found")
    
    return db_spy_cat

@router.put("/spy_cats/{spy_cat_id}", response_model=schemas.SpyCat)
def update_spy_cat(spy_cat_id: int, spy_cat_update: schemas.SpyCatBase, db: Session = Depends(get_db)):
    updated_cat = crud.update_spy_cat(db=db, spy_cat_id=spy_cat_id, spy_cat_update=spy_cat_update)
    
    if not updated_cat:
        raise HTTPException(status_code=404, detail="Spy Cat not found")
    
    return updated_cat

@router.delete("/spy_cats/{spy_cat_id}")
def delete_spy_cat(spy_cat_id: int, db: Session = Depends(get_db)):
    if not crud.delete_spy_cat(db=db, spy_cat_id=spy_cat_id):
        raise HTTPException(status_code=404, detail="Spy Cat not found")
    
    return {"detail": "Spy Cat deleted"}



@router.post("/missions/", response_model=schemas.Mission)
def create_mission(mission: schemas.MissionCreate, db: Session = Depends(get_db)):
    return crud.create_mission(db=db, mission=mission)

@router.get("/missions/", response_model=List[schemas.Mission])
def read_missions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_missions(db=db, skip=skip, limit=limit)

@router.get("/missions/{mission_id}", response_model=schemas.Mission)
def read_mission(mission_id: int, db: Session = Depends(get_db)):
    mission_db = crud.get_mission(db=db, mission_id=mission_id)

    if not mission_db:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    return mission_db

