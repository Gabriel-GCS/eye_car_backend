import math
from typing import List
import motor.motor_asyncio
from bson import ObjectId
from decouple import config
from dtos.ResponseDTO import ResponseDTO
from enums.DbNamesEnum import DbNamesEnum
from database.MongoDB import MongoDB
from utils.AuthUtil import AuthUtil
from utils.ConverterUtil import ConverterUtil

converterUtil = ConverterUtil()
authUtil = AuthUtil()

class UserCarRepository:

    async def add_car_user(self, user_id, car_id):
        try:
            car_user_dict = {
                "user_id" : ObjectId(user_id),
                "car_id" : ObjectId(car_id)
            }
            
            MongoDB().user_car_collection.insert_one(car_user_dict)
        except Exception as error:
            print(error)

    async def found_car_user(self, user_id, car_id):
        try:
            car = MongoDB().user_car_collection.find_one({"user_id": user_id, "car_id": car_id})

            return car
        except Exception as error:
            print(error)
            return ResponseDTO("Internal server error", str(error), 500)
        
    async def list_user_cars(self, user_id):
        try:
            result = MongoDB().user_car_collection.aggregate([
                {
                    "$match" : {
                        "user_id" : ObjectId(user_id)
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

            final_response = []

            for data in result:
                data['_id'] = str(data['_id'])
                data['user_id'] = str(data['user_id'])
                data['car_id'] = str(data['car_id'])
                data['car'][0]['_id'] = str(data['car'][0]['_id'])
                final_response.append(data)

            return final_response
        except Exception as error:
            print(error)
            return ResponseDTO("Internal server error", str(error), 500)

