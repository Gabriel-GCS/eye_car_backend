from fastapi import APIRouter, Depends, HTTPException, Header

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
    
@router.get(
    '/id',
    response_description='Route to list one car',
    dependencies=[Depends(token_verify)]
)
async def info_car(car_id: str, authorization: str = Header(default='')):
    try:
        user_logged = await authService.find_logged_user(authorization)
        result = await carService.find_car(car_id, user_logged.id)

        if not result.status == 200:
             raise HTTPException(status_code=result.status, detail=result.message)
        
        return result

    except Exception as error:
        raise error

        