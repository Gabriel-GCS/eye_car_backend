import os

from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from datetime import datetime
from middlewares.JWTMiddleware import token_verify
from models.UserModel import UserCreateModel, UserUpdateModel
from services.AuthService import AuthService
from services.UserService import UserService

router = APIRouter()

userService = UserService()
authService = AuthService()


# @router.post("/", response_description="Route to create new user")
# async def create_user(file: UploadFile, user: UserCreateModel = Depends(UserCreateModel)):
#     try:
#         photo_route = f'files/photo-{datetime.now().strftime("%H%M%S")}.png'

#         with open(photo_route, 'wb+') as arquive:
#             arquive.write(file.file.read())

#         result = await userService.create_user(user, photo_route)

#         os.remove(photo_route)

#         if not result.status == 201:
#             raise HTTPException(status_code=result.status, detail=result.message)

#         return result
#     except Exception as error:
#         raise error

@router.post("/", response_description="Route to create new user")
async def create_user(user: UserCreateModel = Depends(UserCreateModel)):
    try:

        result = await userService.create_user(user)

        if not result.status == 201:
            raise HTTPException(status_code=result.status, detail=result.message)

        return result
    except Exception as error:
        raise error


@router.get(
    '/me',
    response_description='Route to list logged user info',
    dependencies=[Depends(token_verify)]
    )
async def info_logged_user(authorization: str = Header(default='')):
    try:
        user_logged = await authService.find_logged_user(authorization)
        result = await userService.find_user(user_logged.id)

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)

        return result
    except Exception as error:
        raise error


@router.get(
    '/id/{user_id}',
    response_description='Route to list user info',
    dependencies=[Depends(token_verify)]
    )
async def find_user_info(user_id: str):
    try:
        result = await userService.find_user(user_id)

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)

        return result
    except Exception as error:
        raise error


@router.get(
    '/',
    response_description='Route to list all users',
    dependencies=[Depends(token_verify)]
    )
async def list_users(name: str = None):
    try:
        result = await userService.list_users(name)

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)

        return result
    except Exception as error:
        raise error


@router.put(
    '/update',
    response_description='Route to update logged user',
    dependencies=[Depends(token_verify)]
    )
async def update_user(authorization: str = Header(default=''), user_update: UserUpdateModel = Depends(UserUpdateModel)):
    try:
        user_logged = await authService.find_logged_user(authorization)

        result = await userService.update_user(user_logged.id, user_update)

        if not result.status == 200:
            raise HTTPException(status_code=result.status, detail=result.message)

        return result
    except Exception as error:
        raise error
