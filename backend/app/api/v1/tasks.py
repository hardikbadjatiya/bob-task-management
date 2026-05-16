"""
Task Routes
Handles task CRUD operations and filtering
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.user import User
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskFilter
from app.core.dependencies import get_current_active_user
from app.core.exceptions import NotFoundException, ForbiddenException

router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee_id: Optional[int] = None,
    team_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> List[Task]:
    """
    Get all tasks with optional filtering
    
    Args:
        status: Filter by task status
        priority: Filter by task priority
        assignee_id: Filter by assignee
        team_id: Filter by team
        search: Search in title and description
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of tasks
    """
    query = db.query(Task)
    
    # Apply filters
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assignee_id:
        query = query.filter(Task.assignee_id == assignee_id)
    if team_id:
        query = query.filter(Task.team_id == team_id)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Task.title.ilike(search_pattern)) | 
            (Task.description.ilike(search_pattern))
        )
    
    # Get tasks
    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Task:
    """
    Create a new task
    
    Args:
        task_data: Task creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        The created task
    """
    db_task = Task(
        **task_data.model_dump(exclude={"assignee_id", "team_id"}),
        creator_id=current_user.id,
        assignee_id=task_data.assignee_id,
        team_id=task_data.team_id
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Task:
    """
    Get a specific task by ID
    
    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        The requested task
        
    Raises:
        NotFoundException: If task not found
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise NotFoundException(detail="Task not found")
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Task:
    """
    Update a task
    
    Args:
        task_id: Task ID
        task_data: Task update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        The updated task
        
    Raises:
        NotFoundException: If task not found
        ForbiddenException: If user doesn't have permission
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise NotFoundException(detail="Task not found")
    
    # Check permissions (creator or assignee can update)
    if task.creator_id != current_user.id and task.assignee_id != current_user.id:
        if not current_user.is_superuser:
            raise ForbiddenException(detail="Not enough permissions to update this task")
    
    # Update task fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a task
    
    Args:
        task_id: Task ID
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        NotFoundException: If task not found
        ForbiddenException: If user doesn't have permission
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise NotFoundException(detail="Task not found")
    
    # Check permissions (only creator or superuser can delete)
    if task.creator_id != current_user.id and not current_user.is_superuser:
        raise ForbiddenException(detail="Not enough permissions to delete this task")
    
    db.delete(task)
    db.commit()

# Made with Bob
