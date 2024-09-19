from models.user_model import User


class UserInDB(User):
    hashed_password: str