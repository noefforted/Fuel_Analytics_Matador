# app/schemas.py
from pydantic import BaseModel
from datetime import datetime


class FuelData(BaseModel):
    cycle: int
    cycle_fuel_consumed: float
    cycle_distance: int
    fuel_rate: float
    time_awal: datetime
    time_akhir: datetime
