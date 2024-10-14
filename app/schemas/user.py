def UserSchema(item) -> dict:
    return {
        "id": item.id,
        "username": item.username,
        "email": item.email,
        "is_superuser": item.is_superuser,
        "is_active": item.is_active,
        "is_staff": item.is_staff,
        "is_admin": item.is_admin,
        "date_joined": item.date_joined,
    }
    
def UsersSchema(items) -> list:
    return [UserSchema(item) for item in items]
