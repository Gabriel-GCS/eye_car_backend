import time

import jwt
from decouple import config

from dtos.ResponseDTO import ResponseDTO
from models.UserModel import UserLoginModel, UserModel
from repositories.UserRepository import UserRepository
from services.UserService import UserService
from utils.AuthUtil import AuthUtil

JWT_SECRET = config('JWT_SECRET')

userRepository = UserRepository()

authUtil = AuthUtil()

userService = UserService()


class AuthService:

    def jwt_generate(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "time_expiration": time.time() + 6000
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        return token

    def decode_jwt(self, token: str):
        try:
            decode_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

            if decode_token["time_expiration"] >= time.time():
                return decode_token
            else:
                return None
        except Exception as error:
            print(error)
            return None

    async def login_service(self, user: UserLoginModel):
        user_found = await userRepository.find_user_by_email(user.email)
        
        if not user_found:
            return ResponseDTO("E-mail or password incorrect.", "", 401)
        else:
            if authUtil.check_password(user.password, user_found.password):
                return ResponseDTO("Login successfully!", user_found, 200)
            else:
                return ResponseDTO("E-mail or password incorrect.", "", 401)

    async def find_logged_user(self, authorization: str) -> UserModel:
        token = authorization.split(' ')[1]
        payload = self.decode_jwt(token)

        user_result = await userService.find_user(payload["user_id"])


        logged_user = user_result.data

        return logged_user