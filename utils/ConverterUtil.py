from models.UsuarioModel import UserModel


class ConverterUtil:
    def user_converter(self, usuario):
        return UserModel(
            id=str(usuario["_id"]),
            name=usuario["name"],
            email=usuario["email"],
            password=usuario["password"],
            photo=usuario["photo"] if "photo" in usuario else "",
            token=usuario["token"] if "token" in usuario else "",
        )
