import asyncio

from app.core.database import engine


async def test_connection():
    try:
        connection = await engine.connect()
        print("DATABASE CONNECTED SUCCESSFULLY")
        await connection.close()
    except Exception as error:
        print("DATABASE CONNECTION FAILED")
        print(error)


asyncio.run(test_connection())