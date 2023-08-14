from decouple import config
from pymongo import MongoClient

MONGODB_URL = config("MONGODB_URL")
MONGODB_DB_NAME = config("MONGODB_DB_NAME")


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MongoDB(metaclass=SingletonMeta):
    def __init__(self):
        self.client = MongoClient(MONGODB_URL)
        self.db_name = self.client[MONGODB_DB_NAME]

        self.cars_collection = self.db_name["cars"]
        self.users_collection = self.db_name["users"]
        self.user_car_collection = self.db_name["user_car"]