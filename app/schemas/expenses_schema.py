from pydantic import BaseModel, Field
from datetime import datetime, timezone
# from typing import Literal
from enum import Enum

class CategoryEnum(str, Enum):
    groceries = "groceries"
    leisure = "leisure"
    electronics = "electronics"
    utilities = "utilities"
    clothing = "clothing"
    health = "health"
    others = "others"


class ExpenseCreate(BaseModel):
    description: str = Field(..., min_length=2, max_length=130, examples=["Nuevo gasto por concierto"])
    valor: float = Field(..., gt=0, description="Amount of expense")
    category: CategoryEnum | None = Field(None, description="expense category")
    date: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))


class ExpenseDb(ExpenseCreate):
    user_id: str

class ExpenseOut(ExpenseDb):
    expense_id: str = Field(alias="_id")

    class Config:
        populate_by_name = True


class ExpenseUpdate(BaseModel):
    description: str | None = Field(..., min_length=2, max_length=130, examples=["Nuevo gasto por concierto"])
    valor: float | None = Field(..., gt=0, description="Amount of expense")
    category: CategoryEnum | None = Field(None, description="expense category")
    date: datetime | None = None