import time

import jwt
from decouple import config

from dtos.ResponseDTO import ResponseDTO
from models.UsuarioModel import UsuarioLoginModel, UserModel
from repositories.UserRepository import UserRepository
from services.UserService import UsuarioService
from utils.AuthUtil import AuthUtil

JWT_SECRET = config('JWT_SECRET')

userRepository = UserRepository()

authUtil = AuthUtil()

usuarioService = UsuarioService()


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

    async def login_service(self, usuario: UsuarioLoginModel):
        user_found = await userRepository.buscar_usuario_por_email(usuario.email)

        if not user_found:
            return ResponseDTO("E-mail ou Senha incorretos.", "", 401)
        else:
            if authUtil.verificar_senha(usuario.senha, user_found.senha):
                return ResponseDTO("Login realizado com sucesso!", user_found, 200)
            else:
                return ResponseDTO("E-mail ou Senha incorretos.", "", 401)

    async def find_logged_user(self, authorization: str) -> UserModel:
        token = authorization.split(' ')[1]
        payload = self.decode_jwt(token)

        user_result = await usuarioService.find_user(payload["user_id"])


        usuario_logado = user_result.dados

        return usuario_logado