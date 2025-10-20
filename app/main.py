from fastapi import FastAPI
from app.router.user_router import router as user_router
from app.router.expense_router import router as expense_router

app = FastAPI()

app.include_router(user_router)
app.include_router(expense_router)

@app.get("/")
def root():
    return {"hello":"world"}
