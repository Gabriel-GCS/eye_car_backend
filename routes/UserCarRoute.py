from fastapi import APIRouter, Depends, HTTPException, Header

from middlewares.JWTMiddleware import token_verify
from repositories.HistoricRepository import HistoricRepository
from services.AuthService import AuthService
from services.CarService import CarService
from services.UserCarService import UserCarService

router = APIRouter()
authService = AuthService()
carService = CarService()
userCarService = UserCarService()
historicRepository = HistoricRepository()

@router.put(
    '/add/{car_id}',
    response_description= 'Route to add car to user', 
    dependencies=[Depends(token_verify)]
    )
async def add_car_user (car_id: str, authorization: str = Header(default='')):
    try:
        logged_user = await authService.find_logged_user(authorization)

        result = await userCarService.add_car_user(logged_user.id, car_id)

        if not result.status == 200:
             raise HTTPException(status_code=result.status, detail=result.message)
        
        return result

    except Exception as error:
        raise error
    
@router.get(
    '/list_user_cars',
    response_description= 'Route to list user cars', 
    dependencies=[Depends(token_verify)]
    )
async def list_car_user (authorization: str = Header(default='')):
    try:
        logged_user = await authService.find_logged_user(authorization)

        result = await userCarService.list_user_cars(logged_user.id)

        if not result.status == 200:
             raise HTTPException(status_code=result.status, detail=result.message)
        
        return result

    except Exception as error:
        raise error
    
@router.put(
    '/like/{car_id}',
    response_description= 'Route to like car', 
    dependencies=[Depends(token_verify)]
    )
async def like_car (car_id: str, authorization: str = Header(default='')):
    try:
        logged_user = await authService.find_logged_user(authorization)

        result = await userCarService.like_car(logged_user.id, car_id)

        if not result.status == 200:
             raise HTTPException(status_code=result.status, detail=result.message)
        
        return result

    except Exception as error:
        raise error
    
@router.put(
    '/favorite/{car_id}',
    response_description= 'Route to like car', 
    dependencies=[Depends(token_verify)]
    )
async def like_car (car_id: str, authorization: str = Header(default='')):
    try:
        logged_user = await authService.find_logged_user(authorization)

        result = await userCarService.favorite_car(logged_user.id, car_id)

        if not result.status == 200:
             raise HTTPException(status_code=result.status, detail=result.message)
        
        return result

    except Exception as error:
        raise error
    
@router.get(
    '/historic',
    response_description= 'List historic',
    dependencies=[Depends(token_verify)]
)
async def list_historic (authorization: str = Header(default='')):
    try:
        logged_user = await authService.find_logged_user(authorization)

        result = await historicRepository.list_historic(logged_user.id)
        
        return result

    except Exception as error:
        raise error
        