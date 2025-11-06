from sqlalchemy.orm import Session
from . import models
from passlib.context import CryptContext
from datetime import datetime
import secrets

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username==username).first()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user by username and password"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_user(db: Session, username: str, password: str):
    password = password[:72]  # truncate to max bcrypt length
    hashed_password = pwd_context.hash(password)

    # Generate a random avatar seed
    avatar_seed = secrets.token_urlsafe(8)

    db_user = models.User(
        username=username,
        password_hash=hashed_password,
        total_points=0,
        avatar_style="avataaars",
        avatar_seed=avatar_seed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Initialize default achievements and avatar styles
    initialize_achievements(db)
    initialize_avatar_styles(db)

    return db_user

# API Key functions
def generate_api_key() -> str:
    """Generate a secure random API key"""
    return f"llw_{secrets.token_urlsafe(32)}"

def create_api_key(db: Session, user_id: int, name: str):
    key = generate_api_key()
    api_key = models.APIKey(user_id=user_id, key=key, name=name)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key

def get_user_by_api_key(db: Session, api_key: str):
    key_obj = db.query(models.APIKey).filter(
        models.APIKey.key == api_key,
        models.APIKey.is_active == True
    ).first()

    if key_obj:
        # Update last used timestamp
        key_obj.last_used = datetime.utcnow()
        db.commit()
        return key_obj.user
    return None

def get_user_api_keys(db: Session, user_id: int):
    return db.query(models.APIKey).filter(models.APIKey.user_id == user_id).all()

def revoke_api_key(db: Session, user_id: int, key_id: int):
    key = db.query(models.APIKey).filter(
        models.APIKey.id == key_id,
        models.APIKey.user_id == user_id
    ).first()
    if key:
        key.is_active = False
        db.commit()
        return True
    return False

# Progress tracking functions
def update_progress(db: Session, user_id: int, lesson_id: int, completed: bool, score: int = None):
    progress = db.query(models.Progress).filter(
        models.Progress.user_id == user_id,
        models.Progress.lesson_id == lesson_id
    ).first()

    if not progress:
        progress = models.Progress(
            user_id=user_id,
            lesson_id=lesson_id,
            completed=completed,
            score=score,
            best_score=score,
            attempts=1
        )
        db.add(progress)
    else:
        progress.completed = completed
        progress.attempts += 1
        if score:
            progress.score = score
            if not progress.best_score or score > progress.best_score:
                progress.best_score = score

    if completed:
        progress.completed_at = datetime.utcnow()

    progress.last_practiced = datetime.utcnow()

    db.commit()
    db.refresh(progress)

    # Check for achievements
    check_and_award_achievements(db, user_id)

    return progress

def get_user_progress(db: Session, user_id: int):
    return db.query(models.Progress).filter(models.Progress.user_id == user_id).all()

def get_lesson_progress(db: Session, user_id: int, lesson_id: int):
    return db.query(models.Progress).filter(
        models.Progress.user_id == user_id,
        models.Progress.lesson_id == lesson_id
    ).first()

# Achievement functions
def initialize_achievements(db: Session):
    """Create default achievements if they don't exist"""
    achievements = [
        {"name": "First Steps", "description": "Complete your first lesson", "icon": "🎯", "points": 10, "category": "lessons"},
        {"name": "Dedicated Learner", "description": "Complete 3 lessons", "icon": "📚", "points": 25, "category": "lessons"},
        {"name": "Spanish Master", "description": "Complete all 5 lessons", "icon": "🏆", "points": 50, "category": "lessons"},
        {"name": "Perfect Score", "description": "Get 100% on any quiz", "icon": "⭐", "points": 20, "category": "scores"},
        {"name": "Quiz Champion", "description": "Get 100% on 3 different quizzes", "icon": "🌟", "points": 40, "category": "scores"},
        {"name": "Vocabulary Expert", "description": "Complete all vocabulary lessons", "icon": "📖", "points": 30, "category": "lessons"},
        {"name": "Persistent", "description": "Retry a lesson 5 times", "icon": "💪", "points": 15, "category": "streak"},
        {"name": "Quick Learner", "description": "Complete a lesson on first try with 80%+", "icon": "🚀", "points": 25, "category": "scores"},
        {"name": "Point Collector", "description": "Earn 100 total points", "icon": "💎", "points": 50, "category": "points"},
        {"name": "Practice Makes Perfect", "description": "Complete 10 quiz attempts", "icon": "🎓", "points": 35, "category": "streak"},
    ]

    for ach_data in achievements:
        existing = db.query(models.Achievement).filter(models.Achievement.name == ach_data["name"]).first()
        if not existing:
            achievement = models.Achievement(**ach_data)
            db.add(achievement)

    db.commit()

def check_and_award_achievements(db: Session, user_id: int):
    """Check if user earned any new achievements"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return

    progress_list = get_user_progress(db, user_id)
    completed_lessons = [p for p in progress_list if p.completed]
    perfect_scores = [p for p in progress_list if p.best_score == 5]  # 5 questions per quiz
    total_attempts = sum(p.attempts for p in progress_list)

    # Check achievements
    achievement_checks = {
        "First Steps": len(completed_lessons) >= 1,
        "Dedicated Learner": len(completed_lessons) >= 3,
        "Spanish Master": len(completed_lessons) >= 5,
        "Perfect Score": len(perfect_scores) >= 1,
        "Quiz Champion": len(perfect_scores) >= 3,
        "Persistent": any(p.attempts >= 5 for p in progress_list),
        "Quick Learner": any(p.attempts == 1 and p.best_score and p.best_score >= 4 for p in progress_list),
        "Point Collector": user.total_points >= 100,
        "Practice Makes Perfect": total_attempts >= 10,
    }

    for achievement_name, earned in achievement_checks.items():
        if earned:
            achievement = db.query(models.Achievement).filter(models.Achievement.name == achievement_name).first()
            if achievement:
                # Check if user already has this achievement
                existing = db.query(models.UserAchievement).filter(
                    models.UserAchievement.user_id == user_id,
                    models.UserAchievement.achievement_id == achievement.id
                ).first()

                if not existing:
                    # Award achievement
                    user_achievement = models.UserAchievement(
                        user_id=user_id,
                        achievement_id=achievement.id
                    )
                    db.add(user_achievement)

                    # Add points to user
                    user.total_points += achievement.points

    db.commit()

def get_user_achievements(db: Session, user_id: int):
    """Get all achievements earned by user"""
    user_achievements = db.query(models.UserAchievement).filter(
        models.UserAchievement.user_id == user_id
    ).all()

    return [
        {
            "id": ua.achievement.id,
            "name": ua.achievement.name,
            "description": ua.achievement.description,
            "icon": ua.achievement.icon,
            "points": ua.achievement.points,
            "category": ua.achievement.category,
            "earned_at": ua.earned_at
        }
        for ua in user_achievements
    ]

def get_all_achievements(db: Session):
    """Get all available achievements"""
    return db.query(models.Achievement).all()

def get_user_stats(db: Session, user_id: int):
    """Get comprehensive user statistics"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None

    progress_list = get_user_progress(db, user_id)
    completed_count = len([p for p in progress_list if p.completed])
    achievements_list = get_user_achievements(db, user_id)
    total_achievements = db.query(models.Achievement).count()

    best_scores = [
        {"lesson_id": p.lesson_id, "score": p.best_score, "attempts": p.attempts}
        for p in progress_list if p.best_score
    ]
    best_scores.sort(key=lambda x: x["score"], reverse=True)

    recent_activity = [
        {"lesson_id": p.lesson_id, "last_practiced": p.last_practiced, "completed": p.completed}
        for p in progress_list
    ]
    recent_activity.sort(key=lambda x: x["last_practiced"], reverse=True)

    return {
        "username": user.username,
        "total_points": user.total_points,
        "lessons_completed": completed_count,
        "total_lessons": 5,
        "achievements_count": len(achievements_list),
        "total_achievements": total_achievements,
        "best_scores": best_scores[:5],
        "recent_activity": recent_activity[:10]
    }

# Avatar functions
def initialize_avatar_styles(db: Session):
    """Create default avatar styles"""
    styles = [
        {"name": "Classic", "style_type": "avataaars", "cost": 0, "preview_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=classic", "description": "Classic avatar style - FREE!", "is_premium": False},
        {"name": "Pixel Art", "style_type": "pixel-art", "cost": 50, "preview_url": "https://api.dicebear.com/7.x/pixel-art/svg?seed=pixel", "description": "Retro pixel art style", "is_premium": False},
        {"name": "Bottts", "style_type": "bottts", "cost": 75, "preview_url": "https://api.dicebear.com/7.x/bottts/svg?seed=robot", "description": "Fun robot avatars", "is_premium": False},
        {"name": "Adventurer", "style_type": "adventurer", "cost": 100, "preview_url": "https://api.dicebear.com/7.x/adventurer/svg?seed=adventure", "description": "Adventurous character style", "is_premium": True},
        {"name": "Big Smile", "style_type": "big-smile", "cost": 100, "preview_url": "https://api.dicebear.com/7.x/big-smile/svg?seed=smile", "description": "Cheerful big smile avatars", "is_premium": True},
        {"name": "Lorelei", "style_type": "lorelei", "cost": 125, "preview_url": "https://api.dicebear.com/7.x/lorelei/svg?seed=lorelei", "description": "Elegant illustrated style", "is_premium": True},
        {"name": "Miniavs", "style_type": "miniavs", "cost": 150, "preview_url": "https://api.dicebear.com/7.x/miniavs/svg?seed=mini", "description": "Minimalist avatar style", "is_premium": True},
        {"name": "Shapes", "style_type": "shapes", "cost": 200, "preview_url": "https://api.dicebear.com/7.x/shapes/svg?seed=shapes", "description": "Abstract geometric shapes", "is_premium": True},
    ]

    for style_data in styles:
        existing = db.query(models.AvatarStyle).filter(models.AvatarStyle.name == style_data["name"]).first()
        if not existing:
            style = models.AvatarStyle(**style_data)
            db.add(style)

    db.commit()

def get_all_avatar_styles(db: Session, user_id: int = None):
    """Get all avatar styles, optionally marking which ones the user owns"""
    styles = db.query(models.AvatarStyle).all()

    if user_id:
        purchases = db.query(models.AvatarPurchase).filter(
            models.AvatarPurchase.user_id == user_id
        ).all()
        purchased_ids = {p.avatar_style_id for p in purchases}

        return [
            {
                "id": s.id,
                "name": s.name,
                "style_type": s.style_type,
                "cost": s.cost,
                "preview_url": s.preview_url,
                "description": s.description,
                "is_premium": s.is_premium,
                "is_owned": s.id in purchased_ids or s.cost == 0
            }
            for s in styles
        ]

    return styles

def purchase_avatar_style(db: Session, user_id: int, avatar_style_id: int):
    """Purchase an avatar style with points"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None, "User not found"

    style = db.query(models.AvatarStyle).filter(models.AvatarStyle.id == avatar_style_id).first()
    if not style:
        return None, "Avatar style not found"

    # Check if already purchased
    existing = db.query(models.AvatarPurchase).filter(
        models.AvatarPurchase.user_id == user_id,
        models.AvatarPurchase.avatar_style_id == avatar_style_id
    ).first()
    if existing:
        return None, "Already purchased"

    # Check if user has enough points
    if user.total_points < style.cost:
        return None, f"Not enough points. Need {style.cost}, have {user.total_points}"

    # Deduct points and create purchase
    user.total_points -= style.cost
    purchase = models.AvatarPurchase(user_id=user_id, avatar_style_id=avatar_style_id)
    db.add(purchase)
    db.commit()

    return purchase, None

def update_user_avatar(db: Session, user_id: int, avatar_style: str, avatar_seed: str):
    """Update user's avatar"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None

    # Verify user owns this style
    style = db.query(models.AvatarStyle).filter(models.AvatarStyle.style_type == avatar_style).first()
    if style and style.cost > 0:
        purchase = db.query(models.AvatarPurchase).filter(
            models.AvatarPurchase.user_id == user_id,
            models.AvatarPurchase.avatar_style_id == style.id
        ).first()
        if not purchase:
            return None

    user.avatar_style = avatar_style
    user.avatar_seed = avatar_seed
    db.commit()
    db.refresh(user)
    return user