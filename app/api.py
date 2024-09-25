# app/api.py
from fastapi import FastAPI, HTTPException
from app.models import FuelDataModel
from app.schemas import FuelData
from typing import List

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
async def get_fuel_rate():
    # Kode untuk mendapatkan data dari PostgreSQL jika diperlukan
    pass  # Implementasi di sini jika Anda ingin mengambil data dari database
