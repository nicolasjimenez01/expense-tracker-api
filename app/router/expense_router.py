from fastapi import APIRouter, Depends
from app.services.auth_service import get_current_user
from app.services import expenses_service
from app.schemas.expenses_schema import ExpenseCreate
from typing import Annotated

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/")
def get_expenses(current_user: Annotated[dict, Depends(get_current_user)]):
    return expenses_service.get_expenses(current_user)

@router.post("/")
def create_new_expense(expense: ExpenseCreate, current_user: Annotated[dict, Depends(get_current_user)]):
    return expenses_service.create_expense(expense, current_user)