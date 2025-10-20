from app.config.database import expenses_collection
from app.schemas.expenses_schema import ExpenseCreate, ExpenseDb, ExpenseOut
from app.config.database import expenses_collection


def get_expenses(current_user: dict):
    result = expenses_collection.find({"user_id": str(current_user["_id"])})
    expenses = list(result)
    
    for expense in expenses:
        expense["_id"] = str(expense["_id"])
    return expenses


def create_expense(expense: ExpenseCreate, current_user: dict):
    new_expense = ExpenseDb(
        user_id=str(current_user["_id"]),
        **expense.model_dump(by_alias=True)
    )

    expense_db = expenses_collection.insert_one(new_expense.model_dump())

    if expense_db.inserted_id:
       return ExpenseOut(
            _id=str(expense_db.inserted_id),
            user_id=str(current_user["_id"]),
            **expense.model_dump(by_alias=True)
        )