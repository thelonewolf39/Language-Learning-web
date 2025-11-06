from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    total_points: int
    created_at: datetime
    avatar_style: str
    avatar_seed: Optional[str]
    custom_avatar_url: Optional[str]

    class Config:
        from_attributes = True

class APIKeyCreate(BaseModel):
    name: str

class APIKeyResponse(BaseModel):
    id: int
    key: str
    name: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    lesson_id: int
    completed: bool
    score: Optional[int] = None

class ProgressResponse(BaseModel):
    lesson_id: int
    completed: bool
    score: Optional[int]
    best_score: Optional[int]
    attempts: int
    last_practiced: datetime

    class Config:
        from_attributes = True

class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    points: int
    category: str
    earned_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserStatsResponse(BaseModel):
    username: str
    total_points: int
    lessons_completed: int
    total_lessons: int
    achievements_count: int
    total_achievements: int
    best_scores: List[dict]
    recent_activity: List[dict]

class AvatarStyleResponse(BaseModel):
    id: int
    name: str
    style_type: str
    cost: int
    preview_url: str
    description: str
    is_premium: bool
    is_owned: Optional[bool] = False

    class Config:
        from_attributes = True

class AvatarPurchaseRequest(BaseModel):
    avatar_style_id: int

class AvatarUpdateRequest(BaseModel):
    avatar_style: str
    avatar_seed: str
