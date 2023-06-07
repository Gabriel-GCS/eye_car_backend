from typing import List

import motor.motor_asyncio
from bson import ObjectId

from decouple import config
from models.UserModel import UserCreateModel, UserModel
from utils.AuthUtil import AuthUtil
from utils.ConverterUtil import ConverterUtil

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.eyecar

user_collection = database.get_collection("users")

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

        user_created = await user_collection.insert_one(user_dict)

        new_user = await user_collection.find_one({ "_id": user_created.inserted_id })

        return converterUtil.user_converter(new_user)

    async def list_users(self, name) -> List[UserModel]:
        users_found = user_collection.find({
            "name": {
                "$regex": name,
                '$options': 'i'
            }
        })

        users = []

        async for user in users_found:
            user.append(converterUtil.user_converter(user))

        return users

    async def find_user(self, id: str) -> UserModel:
        user = await user_collection.find_one({"_id": ObjectId(id)})

        if user:
            return converterUtil.user_converter(user)

    async def find_user_by_email(self, email: str) -> UserModel:
        user = await user_collection.find_one({"email": email})

        if user:
            return converterUtil.user_converter(user)

    async def update_user(self, id: str, data_user: dict) -> UserModel:
        if "password" in data_user:
            data_user['password'] = authUtil.password_encrypt(data_user['password'])

        user = await user_collection.find_one({"_id": ObjectId(id)})

        if user:
            await user_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": data_user}
            )

            user_found = await user_collection.find_one({
                "_id": ObjectId(id)
            })

            return converterUtil.user_converter(user_found)

    async def delete_user(self, id: str):
        user = await user_collection.find_one({"_id": ObjectId(id)})

        if user:
            await user_collection.delete_one({"_id": ObjectId(id)})
