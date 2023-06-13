from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()

class CarModel(BaseModel):
    id: str = Field(...)
    brand: str = Field(...)
    model: str = Field(...)
    year: int = Field(...)
    version: str = Field(...)
    price: float = Field(...)

    def __getitem__(self, item):
        return getattr(self, item)
    
    @decoratorUtil.form_body
    class AddCarInfoModel(BaseModel):
        placa: Optional[str]
        cor: Optional[str]
        chassi: Optional[str]