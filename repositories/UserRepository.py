from typing import List

import motor.motor_asyncio
from bson import ObjectId

from decouple import config
from models.UsuarioModel import UserCreateModel, UserModel
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
            "name": user.nome,
            "email": user.email,
            "password": user.password,
        }

        user_created = await user_collection.insert_one(user_dict)

        new_user = await user_collection.find_one({ "_id": user_created.inserted_id })

        return converterUtil.usuario_converter(new_user)

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
            return converterUtil.usuario_converter(user)

    async def find_user_by_email(self, email: str) -> UserModel:
        usuario = await user_collection.find_one({"email": email})

        if usuario:
            return converterUtil.usuario_converter(usuario)

    async def update_user(self, id: str, dados_usuario: dict) -> UserModel:
        if "senha" in dados_usuario:
            dados_usuario['senha'] = authUtil.gerar_senha_criptografada(dados_usuario['senha'])

        usuario = await user_collection.find_one({"_id": ObjectId(id)})

        if usuario:
            await user_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": dados_usuario}
            )

            usuario_encontrado = await user_collection.find_one({
                "_id": ObjectId(id)
            })

            return converterUtil.usuario_converter(usuario_encontrado)

    async def delete_user(self, id: str):
        usuario = await user_collection.find_one({"_id": ObjectId(id)})

        if usuario:
            await user_collection.delete_one({"_id": ObjectId(id)})
