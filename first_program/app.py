# app.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Task, Base
from schemas import TaskCreate, TaskOut

# Initialize FastAPI app
app = FastAPI()

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Dependency to get the database session    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new task
@app.post("/tasks/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(title=task.title, description=task.description, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Get all tasks
@app.get("/tasks/", response_model=list[TaskOut])
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# Get a specific task by ID
@app.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# Update a task's completed status
@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.description = task.description
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)
    return db_task

# Delete a task
@app.delete("/tasks/{task_id}", response_model=TaskOut)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return db_task
