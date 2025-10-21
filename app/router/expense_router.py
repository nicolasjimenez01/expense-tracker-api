from fastapi import APIRouter, Depends
from app.services.auth_service import get_current_user
from app.services import expenses_service
from app.schemas.expenses_schema import ExpenseCreate, ExpenseUpdate, CategoryEnum
from typing import Annotated

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/")
def get_expenses(
    current_user: Annotated[dict, Depends(get_current_user)],
    category: CategoryEnum | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    description: str | None = None,
    min_valor: float | None = None,
    max_valor: float | None = None
):
    return expenses_service.get_expenses(
        current_user=current_user,
        category=category,
        date_from=date_from,
        date_to=date_to,
        description=description,
        min_valor=min_valor,
        max_valor=max_valor
    )

@router.get("/{expense_id}")
def get_expense(expense_id: str, current_user: Annotated[dict, Depends(get_current_user)]):
    return expenses_service.get_expense(expense_id, current_user)


@router.post("/")
def create_new_expense(expense: ExpenseCreate, current_user: Annotated[dict, Depends(get_current_user)]):
    return expenses_service.create_expense(expense, current_user)

@router.delete("/{expense_id}")
def delete_expense(expense_id: str, current_user: Annotated[dict, Depends(get_current_user)]):
    return expenses_service.delete_expense(expense_id, current_user)

@router.patch("/{expense_id}")
def update_expense(expense_id: str, current_user: Annotated[dict, Depends(get_current_user)], expense: ExpenseUpdate):
    return expenses_service.update_expense(expense_id, current_user, expense)
