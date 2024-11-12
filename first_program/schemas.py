# schemas.py
from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

# For creating a task (data will only come from the user when creating)
class TaskCreate(TaskBase):
    pass

# For reading a task (include id)
class TaskOut(TaskBase):
    id: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries
