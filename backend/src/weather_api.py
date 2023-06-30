import requests
import os
from time import time


class WeatherAPI:
    def __init__(self) -> None:
        pass

    def get_weather():
        """
        Gibt die Daten einer bestimmten Wetterstation zurück. Die Wetterstation wird mit Hilfe einer ID angegeben
        """
        AQIN_KEY = os.getenv("AQIN_KEY")
        UmweltstationID = os.getenv("UmweltstationID") 
        response = requests.get(
            f"https://api.waqi.info/feed/@{UmweltstationID}/?token={AQIN_KEY}"
        )
        if response.json()['data'] == "Unknown station":
            print("Fehler bei Station")
            return {"error": "Es wurde keine Umweltstation gefunden"}
        
        data = response.json()['data']
   
        dt = time()
        temp = data['iaqi']['t']['v']
        pressure = data['iaqi']['p']['v']
        wind = data['iaqi']['w']['v']
        weather = {"timestamp":  dt,  "temp": temp, "pressure": pressure, "wind": wind}

        return weather