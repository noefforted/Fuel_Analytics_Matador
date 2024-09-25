# app/api.py
from fastapi import FastAPI, HTTPException, Query
from app.models import FuelDataModel
from app.schemas import FuelData
from typing import List
from datetime import datetime

app = FastAPI()
fuel_data_model = FuelDataModel()


@app.post("/fuel-rate", status_code=201)
async def post_fuel_rate(data: List[FuelData]):
    try:
        await fuel_data_model.save_to_db(data)
        return {"message": "Data berhasil disimpan ke database", "data_count": len(data)}
    except Exception as e:
        print(f"Error saat menyimpan data: {e}")
        raise HTTPException(status_code=500, detail="Gagal menyimpan data")


@app.get("/fuel-rate", response_model=List[FuelData])
async def get_fuel_rate(start_time: datetime = Query(None), end_time: datetime = Query(None)):
    try:
        if not start_time or not end_time:
            raise HTTPException(
                status_code=400, detail="start_time and end_time are required")

        data = await fuel_data_model.get_filtered_data(start_time, end_time)

        if not data:
            raise HTTPException(
                status_code=404, detail="Data not found in the specified datetime range")

        return data
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
