import datetime
from dtos.ResponseDTO import ResponseDTO
from repositories.CarRepository import CarRepository
from repositories.HistoricRepository import HistoricRepository
from services.AuthService import AuthService

authService = AuthService()
carRepository = CarRepository()
historicRepository = HistoricRepository()

class CarService:
    async def find_car(self, id: str, user_id):
        try:
            car_found = await carRepository.find_car(id)

            if car_found:
                await historicRepository.register_historic(user_id, id)

                return ResponseDTO("Car Found.", car_found, 200)
            else:
                return ResponseDTO(f"Car with id {id} not found.", "", 404) 
        except Exception as error:
            print(error)

            return ResponseDTO("Internal server error", str(error), 500)
        
    async def list_car(self,limit, page, order_by, order_type, filter_by, filter_data):
        try:
             
            car_list = await carRepository.car_filter(limit, page, order_by, order_type, filter_by, filter_data)

            return car_list
             
        except Exception as error:
             print(error)