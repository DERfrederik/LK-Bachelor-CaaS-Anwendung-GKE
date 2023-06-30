from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer # OAuth2PasswordRequestForm is a class that represents a form for requesting an OAuth2 access token using a username and password. This form can be used to authenticate users and obtain access tokens that can be used to access protected resources. OAuth2PasswordBearer is a class that represents a security scheme for authenticating API requests using OAuth2 access tokens. This security scheme can be used to protect routes in our FastAPI application that require authentication.
from pydantic import BaseModel, Field  # bietet eine einfache Möglichkeit, Python-Klassen zu definieren, die Datenattribute und deren Typen beschreiben. Mit Pydantic können Entwickler die Eingabevalidierung automatisieren, Daten in verschiedenen Formaten serialisieren und deserialisieren sowie Datenobjekte mit Standardwerten erstellen.
from jose import jwt # Für json webtoken
import datetime
from enum import Enum

app = FastAPI()  

weather = {0: {"timestamp":  1672531261,  "temp": -5, "temp_type": "grad", "pressure": 998, "wind": 14},
1: {"timestamp":  1675209661,  "temp": 4, "temp_type": "grad", "pressure": 1121, "wind": 20},
2: {"timestamp":  1677628861,  "temp": 9, "temp_type": "grad", "pressure": 856, "wind": 37},
3: {"timestamp":  1680303661,  "temp": 13, "temp_type": "grad", "pressure": 1060, "wind": 40},
4: {"timestamp":  1682895661,  "temp": 17, "temp_type": "grad", "pressure": 1201, "wind": 25}}


class TempType(Enum): # Enum um Auswahlmöglichkeiten für bestimmte Felder zu setzen
	grad = "grad"
	fahrenheit = "fahrenheit"

# Wir können genau angeben, wie die Daten aussehen sollen -> Pydantic
class WeatherItem(BaseModel):
	timestamp: datetime.datetime
	temp: int
	temp_type: TempType   # So kann man eine Auswahlmöglichkeit von Werten realisieren
	pressure: int
	wind: int = Field(0, gt=-1, lt=1000000)  # 0 Standardwert, Wert greater than and lower than ... weiter spezifizieren -> kann keinen negativen Wind geben

class ResponseWeahterItem(BaseModel): # Manchmal möchte man nicht alle Ergebnisse zurücklifern, stattdesssen kann man auch eine Teilmenge nehmen, z.B ohne PW
	timestamp: datetime.datetime


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login") # Schema verlinkt auf Endpunkt der den Login macht oder so...

@app.post("/login") # @app.post -> path operation decorator
async def login(data: OAuth2PasswordRequestForm = Depends()): # Für Denpendency Injection
	if data.username == "test" and data.password == "test":
		access_token = jwt.encode({"user": data.username}, key="secret") # Token generieren -> ich glaube der username wird mit dem key "secret" verschlüsselt, ist aber anscheind nicht so sicher, keine sensible Infos in Baerer Token, können leicht decodiert werden
		return {"access_token": access_token, "token_type": "bearer"} # Token zurückgeben
	raise HTTPException( #EIgene Exception werfen
		status_code = status.HTTP_401_UNAUTHORIZED, 
		detail="Incorrect Usernname or Password",
		headers={"WWW-Authentication": "Baerer"}	#Request HEader
	)

# @app.get("/") #Decorator und Pfad
# async def hello(token: str = Depends(oauth2_schema)): # Dpendency injection nur dass man so noch auf den token zugreifen kann, wenn man ihn z.B decodieren möchte
# 	return {"message": "Hello World2!"}

@app.get("/weather/", dependencies=[Depends(oauth2_schema)])  # Dependency Injection -> Endpunkt sichern so wird erst login (user und pw) ausgeführt und danach erhält er den Baerer Token mit dem er an den ENdpunkt kommt -> In der SwaggerUI muss man dann erst auf dass Schloss klicken und seine Nutzerdaten angeben
async def get_all_weather():
	print("Hier")
	return weather

@app.get("/weather_query/")  # Querys werden mit .de:8000/weather_query?=abdas angegben -> kann zum filtern verwendet werden z.B Nach Luftdruck unter 1000 
async def get_query_weather(query: int | None = 0 ): # Hier kommt die Query hin. Durch das Optional lässt sich ein default wert setzten, sonst muss der Nutzer einen wert reinschreiben
	if query:
		data = []
		for weather_key in weather.keys():
			if weather[weather_key]["pressure"] >= query:
				data.append(weather[weather_key])
	return data


@app.get("/weather/{weather_set_id}")
async def get_item(item_id: int): #Hat wirklich Datentypen, die angeben werden können, sonst string und zwar so:
	return weather[item_id]

@app.post("/weather/", response_model=ResponseWeahterItem) # Hier wird angegeben, wie die Antwort aussehen soll (Teilmenge con WheatherItem) 
async def add_weather(data: WeatherItem):	# mit data: sagen wir, dass die erwarteten Daten genauso aussehen solloen, sonst wird ein Fehler geworfen
	highest_id = max(weather.keys())
	weather[highest_id+1] = data
	return data

@app.put("/weather/{weather_set_id}")
async def change_weather(id: int, weather_item: WeatherItem):
	weather[id] = weather_item
	return weather_item

@app.delete("/weather/{weather_set_id}")
async def delete_weather(id: int):
	weather.pop(id, None)
