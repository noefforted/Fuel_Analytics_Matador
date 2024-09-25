# app/database.py
import asyncpg


async def connect_to_db():
    return await asyncpg.connect(
        user='postgres',
        password='0817',
        database='coba',
        host='localhost',           # Gunakan 'localhost' jika database berada di mesin yang sama
        port=5432                   # Port default PostgreSQL
    )
