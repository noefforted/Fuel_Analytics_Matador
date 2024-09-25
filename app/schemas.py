# app/schemas.py
from pydantic import BaseModel
from datetime import datetime


class FuelData(BaseModel):
    Cycle: int
    Cycle_Fuel_Consumed: float
    Cycle_Distance: int
    Fuel_Rate: float
    Time_Awal: datetime
    Time_Akhir: datetime
