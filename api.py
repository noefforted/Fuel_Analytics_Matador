from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd

app = FastAPI()

fuel_data_storage = pd.DataFrame()


class FuelData(BaseModel):
    Cycle: int
    Fuel_Consumed: float
    Fuel_Rate: float
    Time_Awal: str
    Time_Akhir: str


@app.post("/fuel-rate", status_code=201)
def post_fuel_rate(data: List[FuelData]):
    global fuel_data_storage

    # Konversi list dari Pydantic model ke DataFrame
    data_df = pd.DataFrame([item.dict() for item in data])

    if fuel_data_storage.empty:
        fuel_data_storage = data_df
    else:
        fuel_data_storage = pd.concat(
            [fuel_data_storage, data_df], ignore_index=True)

    return {"message": "Data berhasil diterima", "data_count": len(data)}


@app.get("/fuel-rate", response_model=List[FuelData])
def get_fuel_rate():
    global fuel_data_storage

    if fuel_data_storage.empty:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")

    # Mengubah DataFrame menjadi list of dictionaries untuk dikembalikan sebagai response
    return fuel_data_storage.to_dict(orient='records')
