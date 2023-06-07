import os
from datetime import datetime

from bson import ObjectId

from dtos.ResponseDTO import ResponseDTO
from models.UserModel import UserCreateModel, UserUpdateModel
from providers.AWSProvider import AWSProvider
from repositories.UserRepository import UserRepository

awsProvider = AWSProvider()

userRepository = UserRepository()

class UserService:

    async def create_user(self, user: UserCreateModel, photo_path):
        try:
            user_found = await userRepository.find_user_by_email(user.email)

            if user_found:
                return ResponseDTO(f'E-mail {user.email} alredy exist.', "", 400)
            else:
                new_user = await userRepository.create_user(user)

                try:
                    url_photo = awsProvider.upload_arquivo_s3(
                        f'photo-profile/{new_user.id}.png',
                        photo_path
                    )

                    new_user = await userRepository.update_user(new_user.id, {"photo": url_photo})
                except Exception as error:
                    print(error)

                return ResponseDTO("User created successfully", new_user, 201)

        except Exception as error:
            print(error)

            return ResponseDTO("Internal server error", str(error), 500)

    async def find_user(self, id: str):
        try:
            user_found = await userRepository.find_user(id)
            
            if user_found:
                return ResponseDTO("User Found.", user_found, 200)
            else:
                return ResponseDTO(f"User with id {id} not found.", "", 404)

        except Exception as error:
            print(error)

            return ResponseDTO("Internal server error", str(error), 500)

    async def list_users(self, name):
        try:
            users_found = await userRepository.list_users(name)

            return ResponseDTO("User list successfully", users_found, 200)

        except Exception as error:
            print(error)

            return ResponseDTO("Internal server error", str(error), 500)

    async def update_user(self, id, user_update: UserUpdateModel):
        try:
            user_found = await userRepository.find_user(id)

            if user_found:
                user_dict = user_update.__dict__

                try:
                    photo_path = f'files/photo-{datetime.now().strftime("%H%M%S")}.png'

                    with open(photo_path, 'wb+') as arquivo:
                        arquivo.write(user_update.photo.file.read())

                    url_photo = awsProvider.upload_arquivo_s3(
                        f'photo-profile/{id}.png',
                        photo_path
                    )

                    os.remove(photo_path)
                except Exception as error:
                    print(error)

                user_dict['photo'] = url_photo if url_photo is not None else user_dict['photo']

                user_updated = await userRepository.update_user(id, user_dict)

                return ResponseDTO("User updated.", user_updated, 200)
            else:
                return ResponseDTO(f"User with {id} not found.", "", 404)

        except Exception as error:
            print(error)

            return ResponseDTO("Internal server error", str(error), 500)