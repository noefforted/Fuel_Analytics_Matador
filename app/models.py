# app/models.py
from app.database import connect_to_db
from app.schemas import FuelData
from datetime import datetime


class FuelDataModel:
    async def save_to_db(self, data: list[FuelData]):
        connection = await connect_to_db()
        try:
            query_create = '''
                CREATE TABLE IF NOT EXISTS fuel_data (
                id SERIAL PRIMARY KEY,
                cycle INT,
                cycle_fuel_consumed FLOAT,
                cycle_distance INT,
                fuel_rate FLOAT,
                time_awal TIMESTAMPTZ,
                time_akhir TIMESTAMPTZ UNIQUE
                );
                '''
            query_insert = '''
                INSERT INTO fuel_data (cycle, cycle_fuel_consumed, cycle_distance, fuel_rate, time_awal, time_akhir)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (time_akhir) DO NOTHING
                ;
                '''
            await connection.execute(query_create)
            for item in data:
                await connection.execute(query_insert,
                                         item.cycle,
                                         item.cycle_fuel_consumed,
                                         item.cycle_distance,
                                         item.fuel_rate,
                                         item.time_awal,
                                         item.time_akhir)
        finally:
            await connection.close()

    async def get_filtered_data(self, start_time: datetime, end_time: datetime):
        connection = await connect_to_db()
        try:
            query = '''
                SELECT cycle, cycle_fuel_consumed, cycle_distance, fuel_rate, time_awal, time_akhir
                FROM fuel_data
                WHERE time_awal >= $1 AND time_akhir <= $2
                ORDER BY time_awal;
            '''
            rows = await connection.fetch(query, start_time, end_time)
            return [dict(row) for row in rows]
        finally:
            await connection.close()
