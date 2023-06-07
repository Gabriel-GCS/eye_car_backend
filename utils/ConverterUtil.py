from models.UserModel import UserModel


class ConverterUtil:
    def user_converter(self, user):
        return UserModel(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            password=user["password"],
            photo=user["photo"] if "photo" in user else "",
            token=user["token"] if "token" in user else "",
        )
