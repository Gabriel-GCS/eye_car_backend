import math
from typing import List
import motor.motor_asyncio
from bson import ObjectId
from decouple import config
from dtos.ResponseDTO import ResponseDTO
from enums.DbNamesEnum import DbNamesEnum
from utils.AuthUtil import AuthUtil
from utils.ConverterUtil import ConverterUtil

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.eyecar

user_car_collection = database.get_collection("user_car")

converterUtil = ConverterUtil()
authUtil = AuthUtil()

class UserCarRepository:

    async def add_car_user(self, user_id, car_id):
        try:
            car_user_dict = {
                "user" : user_id,
                "car" : car_id
            }
            await user_car_collection.insert_one(car_user_dict)
        except Exception as error:
            print(error)
            return ResponseDTO("Internal server error", str(error), 500)
        
    async def list_user_cars(self, user_id):
        try:
            result = user_car_collection.aggregate([
                {
                    "$match" : {
                        "user" : user_id
                    }
                },
                {
                    "$lookup": {
                        "from": "cars",
                        "localField": "car_id",
                        "foreignField": "_id",
                        "as": "car"
                    }
                }
            ])

            return result
        except Exception as error:
            print(error)
            return ResponseDTO("Internal server error", str(error), 500)

