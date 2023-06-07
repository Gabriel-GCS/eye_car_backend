import os

from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from datetime import datetime
from middlewares.JWTMiddleware import verificar_token
from models.UsuarioModel import UserCreateModel, UsuarioAtualizarModel
from services.AuthService import AuthService
from services.UserService import UsuarioService

router = APIRouter()

userService = UsuarioService()
authService = AuthService()


@router.post("/", response_description="Route to create new user")
async def create_user(file: UploadFile, usuario: UserCreateModel = Depends(UserCreateModel)):
    try:
        photo_route = f'files/photo-{datetime.now().strftime("%H%M%S")}.png'

        with open(photo_route, 'wb+') as arquivo:
            arquivo.write(file.file.read())

        result = await userService.create_user(usuario, photo_route)

        os.remove(photo_route)

        if not result.status == 201:
            raise HTTPException(status_code=result.status, detail=result.mensagem)

        return result
    except Exception as error:
        raise error


@router.get(
    '/me',
    response_description='Route to list user info',
    dependencies=[Depends(verificar_token)]
    )
async def info_logged_user(authorization: str = Header(default='')):
    try:
        usuario_logado = await authService.find_logged_user(authorization)

        resultado = await userService.buscar_usuario(usuario_logado.id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro


@router.get(
    '/{usuario_id}',
    response_description='Rota para buscar as informações do usuário logado.',
    dependencies=[Depends(verificar_token)]
    )
async def buscar_info_usuario(usuario_id: str):
    try:
        resultado = await usuarioService.buscar_usuario(usuario_id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro


@router.get(
    '/',
    response_description='Rota para listar todos usuários.',
    dependencies=[Depends(verificar_token)]
    )
async def listar_usuarios(nome: str):
    try:
        resultado = await usuarioService.listar_usuarios(nome)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro


@router.put(
    '/me',
    response_description='Rota para atualizar as informações do usuário logado.',
    dependencies=[Depends(verificar_token)]
    )
async def atualizar_usuario_logado(authorization: str = Header(default=''), usuario_atualizar: UsuarioAtualizarModel = Depends(UsuarioAtualizarModel)):
    try:
        usuario_logado = await authService.buscar_usuario_logado(authorization)

        resultado = await usuarioService.atualizar_usuario_logado(usuario_logado.id, usuario_atualizar)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro

@router.put(
    '/seguir/{usuario_id}',
    response_description="Rota para follow/unfollow em um usuário.",
    dependencies=[Depends(verificar_token)]
)
async def follow_unfollow_usuario(usuario_id: str, authorization: str = Header(default='')):
    usuario_logado = await authService.buscar_usuario_logado(authorization)

    resultado = await usuarioService.follow_unfollow_usuario(usuario_logado.id, usuario_id)

    if not resultado.status == 200:
        raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

    return resultado
