from typing import List

import motor.motor_asyncio
from bson import ObjectId
from database.MongoDB import MongoDB
from decouple import config
from models.UserModel import UserCreateModel, UserModel
from utils.AuthUtil import AuthUtil
from utils.ConverterUtil import ConverterUtil

converterUtil = ConverterUtil()
authUtil = AuthUtil()


class UserRepository:
    async def create_user(self, user: UserCreateModel) -> UserModel:
        user.password = authUtil.password_encrypt(user.password)

        user_dict = {
            "name": user.name,
            "email": user.email,
            "password": user.password,
        }

        user_created = MongoDB().users_collection.insert_one(user_dict)

        new_user = MongoDB().users_collection.find_one({ "_id": user_created.inserted_id })

        return converterUtil.user_converter(new_user)

    async def list_users(self, name):
        users_found = MongoDB().users_collection.find({
            "name": {
                "$regex": name,
                '$options': 'i'
            }
        })

        users = []

        for user in users_found:
            users.append(converterUtil.user_converter(user))

        return users

    async def find_user(self, id: str) -> UserModel:
        user = MongoDB().users_collection.find_one({"_id": ObjectId(id)})

        if user:
            return converterUtil.user_converter(user)

    async def find_user_by_email(self, email: str) -> UserModel:
        user = MongoDB().users_collection.find_one({"email": email})

        if user:
            return converterUtil.user_converter(user)

    async def update_user(self, id: str, data_user: dict) -> UserModel:
        if "password" in data_user:
            data_user['password'] = authUtil.password_encrypt(data_user['password'])

        user = MongoDB().users_collection.find_one({"_id": ObjectId(id)})

        if user:
            MongoDB().users_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": data_user}
            )

            user_found = MongoDB().users_collection.find_one({
                "_id": ObjectId(id)
            })

            return converterUtil.user_converter(user_found)

    async def delete_user(self, id: str):
        user = MongoDB().users_collection.find_one({"_id": ObjectId(id)})

        if user:
            MongoDB().users_collection.delete_one({"_id": ObjectId(id)})

    async def found_like(self, id: str, car_id:str):
        car = MongoDB().users_collection.find_one({"_id" : ObjectId(id), "likes" : ObjectId(car_id)})
        
        return car
    
    async def remove_like(self, id: str, car_id:str):
        MongoDB().users_collection.update_one(
            {"_id": ObjectId(id)},
            {"$pull": {"likes": ObjectId(car_id)}}
        )

    async def add_like(self, id: str, car_id: str):
        MongoDB().users_collection.update_one(
            {"_id" : ObjectId(id)}, 
            {"$addToSet": {
                "likes" : ObjectId(car_id)
            }}
        )

    async def count_like(self, id: str, car_id: str):

        total = MongoDB().users_collection.aggregate([
            {
            "$addFields": {
                "matching_likes": {
                    "$filter": {
                        "input": "$likes",
                        "as": "like",
                        "cond": { "$eq": ["$$like", ObjectId(car_id)] }
                    }
                }
            }
        },
        {
            "$match": {
                "matching_likes": { "$ne": [] }
            }
        },
        {
            "$count": "total"
        }
        ])

        total = total.next()["total"] if total.alive else 0

        return total
    
    async def found_favorite(self, id: str, car_id:str):
        car = MongoDB().users_collection.find_one({"_id" : ObjectId(id), "favorites" : ObjectId(car_id)})

        return car
    
    async def remove_favorite(self, id: str, car_id:str):
        MongoDB().users_collection.update_one(
            {"_id": ObjectId(id)},
            {"$pull": {"favorites": ObjectId(car_id)}}
        )

    async def add_favorite(self, id: str, car_id: str):
        MongoDB().users_collection.update_one(
            {"_id" : ObjectId(id)}, 
            {"$addToSet": {
                "favorites" : ObjectId(car_id)
            }}
        )

    async def count_favorite(self, id: str, car_id: str):

        total = MongoDB().users_collection.aggregate([
            {
            "$addFields": {
                "matching_favorites": {
                    "$filter": {
                        "input": "$favorites",
                        "as": "favorite",
                        "cond": { "$eq": ["$$favorite", ObjectId(car_id)] }
                    }
                }
            }
        },
        {
            "$match": {
                "matching_favorites": { "$ne": [] }
            }
        },
        {
            "$count": "total"
        }
        ])

        total = total.next()["total"] if total.alive else 0

        return total

