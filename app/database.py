# app/database.py
import asyncpg


async def connect_to_db():
    return await asyncpg.connect(
        user='postgres',           # Ganti dengan nama user PostgreSQL Anda
        password='0817',        # Ganti dengan password PostgreSQL Anda
        database='coba',   # Ganti dengan nama database Anda
        host='localhost',           # Gunakan 'localhost' jika database berada di mesin yang sama
        port=5432                   # Port default PostgreSQL
    )
