from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models, schemas, crud
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = "sqlite:///./data/users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Language-Learning-Web Backend")

# Allow CORS for local dev frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/v1/users/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = crud.create_user(db, user.username, user.password)
    return new_user

@app.get("/api/v1/lessons")
def get_lessons():
    import json
    with open("app/lessons.json") as f:
        lessons = json.load(f)
    return lessons
