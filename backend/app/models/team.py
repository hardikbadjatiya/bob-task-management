"""
Team Model
Represents teams and team memberships for collaboration
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Team(Base):
    """Team model for collaboration"""
    
    __tablename__ = "teams"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Team Details
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="team")
    
    def __repr__(self) -> str:
        return f"<Team(id={self.id}, name='{self.name}')>"


class TeamMember(Base):
    """Team membership model"""
    
    __tablename__ = "team_members"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Membership Details
    is_admin = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")
    
    def __repr__(self) -> str:
        return f"<TeamMember(team_id={self.team_id}, user_id={self.user_id}, is_admin={self.is_admin})>"

# Made with Bob
