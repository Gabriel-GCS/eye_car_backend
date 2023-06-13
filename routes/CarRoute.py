from fastapi import APIRouter, Depends, Header

from middlewares.JWTMiddleware import token_verify
from services.AuthService import AuthService
from services.CarService import CarService

router = APIRouter()
authService = AuthService()
carService = CarService()
    
@router.get(
    '/list',
    response_description='Route to list all cars with filter',
    dependencies=[Depends(token_verify)]
)
async def list_cars(
    authorization: str = Header(default=''),
    limit: int = 10, page: int = 1,
    order_by: str = None,
    order_type: str = None,
    filter_by: str = None,
    filter_data: str = None 
    ):
    try:
        result = await carService.list_car(limit,page,order_by,order_type,filter_by, filter_data)

        return result

    except Exception as error:
        raise error

        