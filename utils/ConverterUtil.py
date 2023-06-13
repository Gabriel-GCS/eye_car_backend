from models.CarModel import CarModel
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
    
    def car_converter(self, car):
        return CarModel(
            id=str(car["_id"]) if "_id" in car else "",
            brand=car["brand"] if "brand" in car else "",
            model=car["model"] if "model" in car else "",
            year=car["year"] if "year" in car else None,
            version=car["version"] if "version" in car else "",
            price=car["price"] if "price" in car else None
        )
