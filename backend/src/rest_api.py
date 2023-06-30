from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
from weather_api import WeatherAPI
from bson import ObjectId
import motor.motor_asyncio
import os

# Der root_path hängt mit dem Proxy zusammen. Dieser wird nur wegen dem Pfad /docs benötigt
# Dieser wird nämlich unter einem anderen Pfad vermutet, da der traefik das /api abschneidet
# Deswegen muss es hier nohcmal angegeben werden
app = FastAPI(root_path="/api")

#DB connection
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_CONN_STRING"])
db = client.weather_db

#weather = {"datetime":  "2023-03-15T12:11:52.436Z",  "temp": -5, "pressure": 998, "wind": 14}

class WeatherItem(BaseModel):
	timestamp: int
	temp: float
	pressure: float
	wind: float

class WeatherError(BaseModel):
	error: str

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/weather/", response_model= WeatherItem | WeatherError)
async def get_weather(timestamp: int | None = None): #Hat wirklich Datentypen, die angeben werden können, sonst string und zwar so:
	if timestamp is None:
		datetime_weather = WeatherAPI.get_weather()
		return datetime_weather
	else:
		# Find the document with the closest timestamp value below the given timestamp
		closest_below = await db["weather"].find_one({"timestamp": {"$lte": timestamp}}, sort=[("timestamp", -1)])
		
		# Find the document with the closest timestamp value above the given timestamp
		closest_above = await db["weather"].find_one({"timestamp": {"$gt": timestamp}}, sort=[("timestamp", 1)])
		
		# Compare the distances of the two documents to the given timestamp
		distance_below = abs(closest_below["timestamp"] - timestamp) if closest_below else float("inf")
		distance_above = abs(closest_above["timestamp"] - timestamp) if closest_above else float("inf")
		
		# Return the document with the closest timestamp value
		if distance_below <= distance_above:
			return closest_below
		else:
			return closest_above