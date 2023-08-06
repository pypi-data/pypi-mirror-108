import requests
import json


class WeatherReport:
    def __init__(self, city):
        self.city = city
        self.api = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?q="
            + self.city+"&appid=60ae5874353359e18d37599372a46659"
        )
        self.data = json.loads(self.api.content)

    def Temperature(self, inkelvin=True):
        temp = int(self.data["main"]["temp"])
        if not inkelvin:
            return int(temp - 273)
        else:
            return temp

    def Humidity(self):
        hum = int(self.data["main"]["humidity"])
        return hum

    def Pressure(self):
        pre = int(self.data["main"]["pressure"])
        return pre

    def WindSpeed(self):
        spe = int(self.data["wind"]["speed"])
        return spe

    def WindDegree(self):
        deg = int(self.data["wind"]["deg"])
        return deg 

