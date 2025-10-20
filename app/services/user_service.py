from app.config.database import users_collection
from app.schemas import user_schema
from fastapi import HTTPException, status
from app.services.auth_service import password_hash

def create_user(data: user_schema.UserDb):

    user_exist = users_collection.find_one({
    "$or": [
        {"name": data.name},
        {"email": data.email}
    ]
    })

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or Email already exist"
        )
    

    new_userdb = user_schema.UserDb(
        name=data.name,
        email=data.email,
        edad=data.edad,
        username=data.username,
        password= password_hash.hash(data.password)
    )


    try:
        new_user = users_collection.insert_one(new_userdb.model_dump())
        if new_user.inserted_id:
            return user_schema.UserOut(
                _id=str(new_user.inserted_id),
                **data.model_dump(by_alias=True)
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


def list_users():
    return list(users_collection.find({}, {"_id": 0}))