import requests

sity = "Санкт-петербург"

url = f"https://api.openweathermap.org/data/2.5/weather?q={sity}&units=metric&lang=ru&appid=c38e5a3db7bd33d13d9d0c37f83ccdec"
weather_data = requests.get(url).json()

print(weather_data)