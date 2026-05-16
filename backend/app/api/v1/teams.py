"""
Team Routes
Handles team and team membership management
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.team import Team, TeamMember
from app.core.dependencies import get_current_active_user
from app.core.exceptions import NotFoundException, ForbiddenException, ConflictException

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_user_teams(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> List[dict]:
    """
    Get all teams for current user
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of teams with membership info
    """
    memberships = db.query(TeamMember).filter(
        TeamMember.user_id == current_user.id
    ).all()
    
    teams = []
    for membership in memberships:
        team = membership.team
        teams.append({
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "is_admin": membership.is_admin,
            "joined_at": membership.joined_at,
            "created_at": team.created_at
        })
    
    return teams


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_team(
    name: str,
    description: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Create a new team
    
    Args:
        name: Team name
        description: Team description
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        The created team
    """
    # Create team
    db_team = Team(name=name, description=description)
    db.add(db_team)
    db.flush()
    
    # Add creator as admin
    membership = TeamMember(
        team_id=db_team.id,
        user_id=current_user.id,
        is_admin=True
    )
    db.add(membership)
    db.commit()
    db.refresh(db_team)
    
    return {
        "id": db_team.id,
        "name": db_team.name,
        "description": db_team.description,
        "created_at": db_team.created_at
    }


@router.get("/{team_id}", response_model=dict)
async def get_team(
    team_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Get team details
    
    Args:
        team_id: Team ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Team details with members
        
    Raises:
        NotFoundException: If team not found
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise NotFoundException(detail="Team not found")
    
    # Get members
    members = []
    for membership in team.members:
        members.append({
            "user_id": membership.user_id,
            "email": membership.user.email,
            "full_name": membership.user.full_name,
            "is_admin": membership.is_admin,
            "joined_at": membership.joined_at
        })
    
    return {
        "id": team.id,
        "name": team.name,
        "description": team.description,
        "created_at": team.created_at,
        "members": members
    }


@router.post("/{team_id}/members", status_code=status.HTTP_201_CREATED)
async def add_team_member(
    team_id: int,
    user_id: int,
    is_admin: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Add a member to team
    
    Args:
        team_id: Team ID
        user_id: User ID to add
        is_admin: Whether user should be admin
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        The created membership
        
    Raises:
        NotFoundException: If team or user not found
        ForbiddenException: If current user is not team admin
        ConflictException: If user is already a member
    """
    # Check if team exists
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise NotFoundException(detail="Team not found")
    
    # Check if current user is admin
    current_membership = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not current_membership or not current_membership.is_admin:
        raise ForbiddenException(detail="Only team admins can add members")
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException(detail="User not found")
    
    # Check if already a member
    existing = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()
    
    if existing:
        raise ConflictException(detail="User is already a team member")
    
    # Add member
    membership = TeamMember(
        team_id=team_id,
        user_id=user_id,
        is_admin=is_admin
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    
    return {
        "team_id": team_id,
        "user_id": user_id,
        "is_admin": is_admin,
        "joined_at": membership.joined_at
    }


@router.delete("/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_team_member(
    team_id: int,
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> None:
    """
    Remove a member from team
    
    Args:
        team_id: Team ID
        user_id: User ID to remove
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        NotFoundException: If team or membership not found
        ForbiddenException: If current user is not team admin
    """
    # Check if current user is admin
    current_membership = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not current_membership or not current_membership.is_admin:
        raise ForbiddenException(detail="Only team admins can remove members")
    
    # Find membership to remove
    membership = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()
    
    if not membership:
        raise NotFoundException(detail="Team membership not found")
    
    db.delete(membership)
    db.commit()

# Made with Bob
