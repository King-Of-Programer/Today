from fastapi import FastAPI
from .database import engine, Base
from .routes import router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
   return {"message": "Welcome to the Spy Cat Agency API!"}