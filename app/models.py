# app/models.py
from app.database import connect_to_db
from app.schemas import FuelData


class FuelDataModel:
    async def save_to_db(self, data: list[FuelData]):
        connection = await connect_to_db()
        try:
            query = '''
                INSERT INTO fuel_data (cycle, cycle_fuel_consumed, cycle_distance, fuel_rate, time_awal, time_akhir)
                VALUES ($1, $2, $3, $4, $5, $6);
            '''
            for item in data:
                await connection.execute(query,
                                         item.Cycle,
                                         item.Cycle_Fuel_Consumed,
                                         item.Cycle_Distance,
                                         item.Fuel_Rate,
                                         item.Time_Awal,
                                         item.Time_Akhir)
        finally:
            await connection.close()
