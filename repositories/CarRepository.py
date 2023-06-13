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

car_collection = database.get_collection("cars")

converterUtil = ConverterUtil()
authUtil = AuthUtil()

class CarRepository:
    async def find_car(self, id : str):
        try:
            car = await car_collection.find_one({"_id" : ObjectId(id)})
            return converterUtil.car_converter(car)
        
        except Exception as error:
            print(error)
            return ResponseDTO("Internal server error", str(error), 500)
        
    async def update_like_car(car_id : str, total: int):
        try:
            
            await car_collection.update_one({"_id" : ObjectId(car_id)}, {"likes" : total})

        except Exception as error:
            print(error)
            return ResponseDTO("Internal server error", str(error), 500)
        
    async def update_favorite_car(car_id : str, total: int):
        try:
            
            await car_collection.update_one({"_id" : ObjectId(car_id)}, {"favorites" : total})

        except Exception as error:
            print(error)
            return ResponseDTO("Internal server error", str(error), 500)
        
    async def car_filter(self, limit, page, order_by, order_type, filter_by, filter_data):
        try:
            skip = (page - 1) * limit
            filter_query = {"$match" : {}}
            order_query = { "$sort" : { "model" : 1} }
            project_query = {
                "$project" : {
                    "id" : 1,
                    "brand" : 1,
                    "model" : 1,
                    "year" : 1,
                    "version" : 1,
                    "price" : 1,
                    str(filter_by) : 1,
                    str(order_by) : 1
                }
            }

            if order_by:
                order_query["$sort"] = {DbNamesEnum.field.value[order_by]: -int(order_type)}

            if filter_by:
                filter_query["$match"] = {DbNamesEnum.field.value[filter_by]: {
                    "$regex" : filter_data,
                    "$options" : 'i'
                }
            }

            total = car_collection.aggregate([
                project_query,
                filter_query,
                {
                    "$count" : "total"
                }
            ])

            total = total.next()["total"] if total.alive else 0

            if total == 0:
                return {
                    "data": [],
                    "pages": 0,
                    "total": 0
                }

            response = car_collection.aggregate([
                project_query,
                filter_query,
                order_query,
                {
                    "$skip" : skip
                },
                {
                    "$limit" : limit
                }
            ])
            pages = math.ceil(total / limit)

            return {
                "data": [],
                "pages": pages,
                "total": total
            }

        except Exception as error:
            print(error)
            return ResponseDTO("Internal server error", str(error), 500)


