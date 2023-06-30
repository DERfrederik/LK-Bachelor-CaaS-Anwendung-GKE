import os
import motor.motor_asyncio
from weather_api import WeatherAPI
import asyncio
from bson import ObjectId
from pydantic import BaseModel, Field

# Database Connection
connection_str = f"mongodb://{os.environ['MONGO_INITDB_ROOT_USERNAME']}:{os.environ['MONGO_INITDB_ROOT_PASSWORD']}@{os.environ['MONGO_URL']}:{os.environ['MONGO_PORT']}"
client = motor.motor_asyncio.AsyncIOMotorClient(connection_str)
db = client.weather_db

#Pydantic 
class Weather(BaseModel):
    timestamp: int
    temp: float
    pressure: float
    wind: float

async def weather_scraper():
    print("start weather scraper")
    while True:
        weather = WeatherAPI.get_weather()
        current_weather = Weather(**weather)
        new_weather = await db["weather"].insert_one(current_weather.dict()) 
        created_weather = await db["weather"].find_one({"_id": ObjectId(new_weather.inserted_id)})
        print("Wetter created", created_weather)
        await asyncio.sleep(3600)

async def weather_scraper_main():
    await weather_scraper()

if __name__ == '__main__':
    asyncio.run(weather_scraper_main())