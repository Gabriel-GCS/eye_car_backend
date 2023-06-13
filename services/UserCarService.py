from dtos.ResponseDTO import ResponseDTO
from repositories.CarRepository import CarRepository
from repositories.UserCarRepository import UserCarRepository
from repositories.UserRepository import UserRepository


userCarRepository = UserCarRepository()
carRepository = CarRepository()
userRepository = UserRepository()

class UserCarService:
        
    async def add_car_user(self, id: str, car_id: str):
        try:
            car_found = await carRepository.find_car(car_id)

            await userCarRepository.add_car_user(id, car_found.id)

            return ResponseDTO("car add to user", "", 200)

        except Exception as error:
            print(error)

            return ResponseDTO("Internal server error", str(error), 500)
        
    async def list_user_cars (self, id: str):
        try:

            result = userCarRepository.list_user_cars(id)

            return ResponseDTO("car add to user", result, 200)

        except Exception as error:
            print(error)

            return ResponseDTO("Internal server error", str(error), 500)
        
    async def like_car(self, id:str, car_id: str):
        try:
            car_found = await carRepository.find_car(car_id)
            found_like = await userRepository.found_like(id, car_found.id)

            if found_like:
                await userRepository.remove_like(id, car_found.id)

            else:
                await userRepository.add_like(id, car_found.id)

            total = await userRepository.count_like(id, car_found.id)

            await carRepository.update_like_car(car_found.id, total)

            return ResponseDTO("car liked", "", 200)
                 
        except Exception as error:
             print(error)

    async def favorite_car(self, id:str, car_id: str):
        try:
            car_found = await carRepository.find_car(car_id)
            found_favorite = await userRepository.found_favorite(id, car_found.id)

            if found_favorite:
                await userRepository.remove_favorite(id, car_found.id)

            else:
                await userRepository.add_favorite(id, car_found.id)

            total = await userRepository.count_favorite(id, car_found.id)

            await carRepository.update_favorite_car(car_found.id, total)

            return ResponseDTO("car liked", "", 200)
                 
        except Exception as error:
             print(error)