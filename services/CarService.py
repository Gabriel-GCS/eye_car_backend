from dtos.ResponseDTO import ResponseDTO
from repositories.CarRepository import CarRepository


carRepository = CarRepository()

class CarService:
    async def find_car(self, id: str):
        try:
            car_found = await carRepository.find_car(id)

            if car_found:
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