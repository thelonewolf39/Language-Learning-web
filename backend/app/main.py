from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app import models, schemas, crud
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import json

DATABASE_URL = "sqlite:///./data/users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Language-Learning-Web API",
    description="Developer-friendly API for Spanish learning with progress tracking, achievements, and avatar shop",
    version="2.0.0"
)

# Allow CORS for local dev frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory session store (in production, use Redis or similar)
active_sessions = {}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication dependencies
def get_current_user_from_session(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get user from session token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    user_id = active_sessions.get(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def get_current_user_from_api_key(
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get user from API key (for developer API)"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")

    user = crud.get_user_by_api_key(db, x_api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return user

# ==================== User Management ====================

@app.post("/api/v1/users/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = crud.create_user(db, user.username, user.password)
    return new_user

@app.post("/api/v1/users/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login and get a session token"""
    authenticated_user = crud.authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate session token
    import secrets
    token = secrets.token_urlsafe(32)
    active_sessions[token] = authenticated_user.id

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": authenticated_user.id,
            "username": authenticated_user.username,
            "total_points": authenticated_user.total_points,
            "avatar_style": authenticated_user.avatar_style,
            "avatar_seed": authenticated_user.avatar_seed
        }
    }

@app.post("/api/v1/users/logout")
def logout_user(authorization: Optional[str] = Header(None)):
    """Logout and invalidate session"""
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        active_sessions.pop(token, None)
    return {"message": "Logged out successfully"}

@app.get("/api/v1/users/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(get_current_user_from_session)):
    """Get current user info"""
    return current_user

# ==================== API Key Management (User must be logged in) ====================

@app.post("/api/v1/api-keys", response_model=schemas.APIKeyResponse)
def create_api_key(
    key_data: schemas.APIKeyCreate,
    current_user: models.User = Depends(get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """Create a new API key (requires login)"""
    api_key = crud.create_api_key(db, current_user.id, key_data.name)
    return api_key

@app.get("/api/v1/api-keys", response_model=List[schemas.APIKeyResponse])
def list_api_keys(
    current_user: models.User = Depends(get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """List all API keys for current user"""
    return crud.get_user_api_keys(db, current_user.id)

@app.delete("/api/v1/api-keys/{key_id}")
def revoke_api_key(
    key_id: int,
    current_user: models.User = Depends(get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """Revoke an API key"""
    success = crud.revoke_api_key(db, current_user.id, key_id)
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")
    return {"message": "API key revoked successfully"}

# ==================== Lessons (Public) ====================

@app.get("/api/v1/lessons")
def get_lessons():
    """Get all available lessons (no auth required)"""
    with open("app/lessons.json") as f:
        lessons = json.load(f)
    return lessons

@app.get("/api/v1/lessons/{lesson_id}")
def get_lesson(lesson_id: int):
    """Get a specific lesson by ID (no auth required)"""
    with open("app/lessons.json") as f:
        lessons = json.load(f)

    lesson = next((l for l in lessons if l["id"] == lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return lesson

# ==================== Progress Tracking (Developer API - requires API key) ====================

@app.get("/api/v1/progress", response_model=List[schemas.ProgressResponse])
def get_user_progress_api(
    current_user: models.User = Depends(get_current_user_from_api_key),
    db: Session = Depends(get_db)
):
    """
    Get all lesson progress for authenticated user (requires API key)

    **Developer API**: Use X-API-Key header
    """
    progress = crud.get_user_progress(db, current_user.id)
    return progress

@app.get("/api/v1/progress/{lesson_id}", response_model=schemas.ProgressResponse)
def get_lesson_progress_api(
    lesson_id: int,
    current_user: models.User = Depends(get_current_user_from_api_key),
    db: Session = Depends(get_db)
):
    """Get progress for a specific lesson (requires API key)"""
    progress = crud.get_lesson_progress(db, current_user.id, lesson_id)
    if not progress:
        raise HTTPException(status_code=404, detail="No progress found for this lesson")
    return progress

@app.post("/api/v1/progress", response_model=schemas.ProgressResponse)
def update_progress_api(
    progress_data: schemas.ProgressUpdate,
    current_user: models.User = Depends(get_current_user_from_api_key),
    db: Session = Depends(get_db)
):
    """
    Update lesson progress (requires API key)

    **Automatically checks and awards achievements!**
    """
    progress = crud.update_progress(
        db,
        current_user.id,
        progress_data.lesson_id,
        progress_data.completed,
        progress_data.score
    )
    return progress

# ==================== Achievements ====================

@app.get("/api/v1/achievements")
def get_all_achievements_api(db: Session = Depends(get_db)):
    """Get all available achievements (no auth required)"""
    achievements = crud.get_all_achievements(db)
    return achievements

@app.get("/api/v1/achievements/user", response_model=List[schemas.AchievementResponse])
def get_user_achievements_api(
    current_user: models.User = Depends(get_current_user_from_api_key),
    db: Session = Depends(get_db)
):
    """Get all achievements earned by authenticated user (requires API key)"""
    achievements = crud.get_user_achievements(db, current_user.id)
    return achievements

# ==================== User Statistics ====================

@app.get("/api/v1/stats", response_model=schemas.UserStatsResponse)
def get_user_stats_api(
    current_user: models.User = Depends(get_current_user_from_api_key),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive user statistics (requires API key)

    **Returns**: Total points, lessons completed, achievements, best scores, recent activity
    """
    stats = crud.get_user_stats(db, current_user.id)
    if not stats:
        raise HTTPException(status_code=404, detail="User not found")
    return stats

# ==================== Avatar Shop ====================

@app.get("/api/v1/avatar-styles", response_model=List[schemas.AvatarStyleResponse])
def get_avatar_styles(
    current_user: models.User = Depends(get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """Get all avatar styles with ownership status"""
    styles = crud.get_all_avatar_styles(db, current_user.id)
    return styles

@app.post("/api/v1/avatar-styles/purchase")
def purchase_avatar(
    purchase: schemas.AvatarPurchaseRequest,
    current_user: models.User = Depends(get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """Purchase an avatar style with points"""
    result, error = crud.purchase_avatar_style(db, current_user.id, purchase.avatar_style_id)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "Avatar style purchased successfully", "remaining_points": current_user.total_points}

@app.put("/api/v1/users/avatar")
def update_avatar(
    avatar_data: schemas.AvatarUpdateRequest,
    current_user: models.User = Depends(get_current_user_from_session),
    db: Session = Depends(get_db)
):
    """Update user's avatar"""
    user = crud.update_user_avatar(db, current_user.id, avatar_data.avatar_style, avatar_data.avatar_seed)
    if not user:
        raise HTTPException(status_code=400, detail="Cannot update avatar - style not owned")
    return {"message": "Avatar updated successfully", "avatar_url": f"https://api.dicebear.com/7.x/{user.avatar_style}/svg?seed={user.avatar_seed}"}

# ==================== Health Check ====================

@app.get("/")
def root():
    return {
        "message": "Language Learning Web API",
        "version": "2.0.0",
        "docs": "/docs",
        "features": [
            "User authentication (login/logout)",
            "API key authentication for developers",
            "Progress tracking",
            "10+ unlockable achievements",
            "Avatar shop with 8 styles",
            "Comprehensive statistics",
            "Points-based reward system"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "sessions": len(active_sessions)}
