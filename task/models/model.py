from datetime import datetime
from pydantic import BaseModel, PositiveInt, Field, ConfigDict
from pydantic import ValidationError
from typing import Annotated, Literal, List
from annotated_types import Gt, Ge, Le
from pydantic import StringConstraints

class TaskInsert(BaseModel):
    text: str
    done: bool

# task 1개
class Task(TaskInsert):
    id: int