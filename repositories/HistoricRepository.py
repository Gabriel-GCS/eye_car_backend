import math
from typing import List
import motor.motor_asyncio
from bson import ObjectId
from datetime import datetime
from database.MongoDB import MongoDB
from decouple import config
from dtos.ResponseDTO import ResponseDTO
from enums.DbNamesEnum import DbNamesEnum
from utils.AuthUtil import AuthUtil
from utils.ConverterUtil import ConverterUtil


converterUtil = ConverterUtil()
authUtil = AuthUtil()

class HistoricRepository:
    async def register_historic(self, user_id : str, car_id):
        
        try:
            found_historic = MongoDB().historic_collection.find_one({'user_id' : user_id, 'car_id': car_id})
            
            if found_historic:
                MongoDB().historic_collection.update_one({'_id': found_historic['_id']}, {'$set': {'date': datetime.now()}})
            
            else:
                historic = {
                    'user_id': user_id,
                    'car_id': car_id,
                    'date': datetime.now()
                }
                MongoDB().historic_collection.insert_one(historic)
        
        except Exception as error:
            print(error)
            return ResponseDTO("Internal server error", str(error), 500)
        
    async def list_historic(self, user_id : str):
        try:
            historic = list(MongoDB().historic_collection.find({'user_id': user_id}))
            final_response = []
            for data in historic:
                cars = list(MongoDB().cars_collection.aggregate([
                    {
                        "$project" : {
                            '_id' : 1,
                            'Marca' : 1,
                            'Modelo' : 1,
                            'Ano' : 1
                        }
                    },
                    {
                        '$match' : {
                            '_id' : ObjectId(data['car_id'])
                        }
                    }
                ]))
                
                cars[0]['date'] = historic[0]['date']
                cars[0]['_id'] = str(cars[0]['_id'])
                final_response.append(cars[0])

            return final_response
            
        except Exception as error:
            print(error)
            return ResponseDTO("Internal server error", str(error), 500)
        

