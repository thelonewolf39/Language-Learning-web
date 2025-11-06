from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_points = Column(Integer, default=0)
    avatar_style = Column(String, default="avataaars")  # DiceBear style
    avatar_seed = Column(String, nullable=True)  # Random seed for avatar
    custom_avatar_url = Column(String, nullable=True)  # Custom uploaded avatar

    # Relationships
    progress = relationship("Progress", back_populates="user")
    api_keys = relationship("APIKey", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    purchases = relationship("AvatarPurchase", back_populates="user")

class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="api_keys")

class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer)
    completed = Column(Boolean, default=False)
    score = Column(Integer, nullable=True)
    best_score = Column(Integer, nullable=True)
    attempts = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)
    last_practiced = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress")

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    icon = Column(String)
    points = Column(Integer, default=10)
    category = Column(String)

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    earned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement")

class AvatarStyle(Base):
    __tablename__ = "avatar_styles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    style_type = Column(String)  # DiceBear style name
    cost = Column(Integer, default=0)  # Point cost (0 = free)
    preview_url = Column(String)
    description = Column(String)
    is_premium = Column(Boolean, default=False)

class AvatarPurchase(Base):
    __tablename__ = "avatar_purchases"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    avatar_style_id = Column(Integer, ForeignKey("avatar_styles.id"))
    purchased_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="purchases")
    avatar_style = relationship("AvatarStyle")
