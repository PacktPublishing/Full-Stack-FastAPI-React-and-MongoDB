from enum import Enum
from typing import List
from pydantic import BaseModel


class Fuel(str, Enum):
    PETROL = 'PETROL'
    DIESEL = 'DIESEL'
    LPG = 'LPG'

class Car:
    brand: str
    model: str
    year: int
    fuel: Fuel
    countries: List[str]

car = Car(
    brand="Lancia",
    model="Musa",
    fuel="PETROL",
    year="2006",
    countries=["Italy","France"]
    )

print(car.json())

try:
    invalid_car = InsertCar(
        brand="Lancia",
        fuel="PETROL",
        year="something",
        countries=["Italy","France"]
    )
except ValidationError as e:
    print(e)
