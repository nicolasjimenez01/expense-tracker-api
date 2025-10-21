from app.config.database import expenses_collection
from app.schemas.expenses_schema import ExpenseCreate, ExpenseDb, ExpenseOut, ExpenseUpdate, CategoryEnum
from pymongo.errors import PyMongoError
from fastapi import HTTPException, status
from bson.objectid import ObjectId
from typing import Any


def build_expense_filter(
    user_id: str,
    category: CategoryEnum | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    description: str | None = None,
    min_valor: float | None = None,
    max_valor: float | None = None
) -> dict[str, Any]:
    """Construye filtro dinámico para consultas de expenses"""
    filter_query: dict[str, Any] = {"user_id": user_id}
    
    if category:
        filter_query["category"] = category
    
    if description:
        filter_query["description"] = {"$regex": description, "$options": "i"}
    
    if date_from or date_to:
        date_filter: dict[str, Any] = {}
        if date_from:
            date_filter["$gte"] = date_from
        if date_to:
            date_filter["$lte"] = date_to
        filter_query["date"] = date_filter
    
    if min_valor or max_valor:
        valor_filter: dict[str, Any] = {}
        if min_valor:
            valor_filter["$gte"] = min_valor
        if max_valor:
            valor_filter["$lte"] = max_valor
        filter_query["valor"] = valor_filter
    
    return filter_query


def get_expenses(
    current_user: dict,
    category: CategoryEnum | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    description: str | None = None,
    min_valor: float | None = None,
    max_valor: float | None = None
):
    try:
        user_id = str(current_user["_id"])
        
        # Construir filtro dinámicamente
        filter_query = build_expense_filter(
            user_id=user_id,
            category=category,
            date_from=date_from,
            date_to=date_to,
            description=description,
            min_valor=min_valor,
            max_valor=max_valor
        )
        
        result = expenses_collection.find(filter_query)
        expenses = list(result)
        
        for expense in expenses:
            expense["_id"] = str(expense["_id"])
        return expenses
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {type(e).__name__} - {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {type(e).__name__} - {str(e)}"
        )

def get_expense(expense_id: str, current_user: dict):
    user_id = str(current_user["_id"])
    obj_id = ObjectId(expense_id)
    expense =  expenses_collection.find_one({
            "_id": obj_id,
            "user_id": user_id
        })
    
    if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found or you don't have permission to view it"
            )
    
    expense["_id"] = str(expense["_id"])
    return expense

def create_expense(expense: ExpenseCreate, current_user: dict):
    try:
        user_id = str(current_user["_id"])
        
        new_expense = ExpenseDb(
            user_id=user_id,
            **expense.model_dump(by_alias=True)
        )

        expense_db = expenses_collection.insert_one(new_expense.model_dump())

        if expense_db.inserted_id:
            return ExpenseOut(
                _id=str(expense_db.inserted_id),
                user_id=user_id,
                **expense.model_dump(by_alias=True)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create expense"
            )
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {type(e).__name__} - {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {type(e).__name__} - {str(e)}"
        )
    
def delete_expense(expense_id: str, current_user: dict):
    try:
        user_id = str(current_user["_id"])
        obj_id = ObjectId(expense_id)
        deleted_expense = expenses_collection.delete_one({
            "_id": obj_id,
            "user_id":user_id
        })

        if deleted_expense.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not foun or don't have permission to delete it"
            )

        return {"message": "Expense deleted successfully", "deleted_count": deleted_expense.deleted_count} 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {type(e).__name__} - {str(e)}"
        )
    
def update_expense(expense_id: str, current_user: dict, new_expense: ExpenseUpdate):

    try:
        user_id = str(current_user["_id"])

        update_data = {"$set": new_expense.model_dump(by_alias=True)}

        resultado = expenses_collection.update_one(
            {"_id": ObjectId(expense_id), "user_id": user_id},
            update_data
        )

        if resultado.matched_count == 0 or resultado.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document not found or not modified"
            )
    
        return {"message": "Document updated correctly", "updated count": resultado.matched_count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {type(e).__name__} - {str(e)}"
        )