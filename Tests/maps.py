from requests import get
from datetime import datetime

sity = "Санкт-петербург"
url = f'http://api.openweathermap.org/data/2.5/forecast?q={sity}&units=metric&lang=ru&appid=dfe5e468eadee1e20ded5140d398450c'

weather_data = get(url).json()

for i in range(len(weather_data['list'])):
    if str(weather_data['list'][i]["dt_txt"]).split()[0] == str(datetime.now()).split()[0]:
        main_weather = str(weather_data['list'][i]['weather'][0]['description'])
        temperature = str(round(weather_data['list'][i]['main']['temp']))
        humidity = str(weather_data['list'][i]['main']['humidity'])
        wind = str(weather_data['list'][i]['wind']['speed'])
        bar = str(round(weather_data['list'][i]['main']['pressure'] * 0.750062, 1))
        vid = str(weather_data['list'][i]['visibility'] / 1000)
        
        weather_split = main_weather.split()
        text = " ".join(weather_split[1:len(weather_split)])
        main_weather = f"{weather_split[0].title()} {text}"
        
        date = str(weather_data['list'][i]["dt_txt"]).split().pop(1)
        
        text_weather = (f"""\n{date}:```День: 
☂ Погода: {main_weather.title()}
℃ Температура: {temperature} °C 
☰ Влажность: {humidity}% 
๑ Ветер: {wind}m/s 
⍗ Давление: {bar}мм.рт.ст 
☁ Видимость: {vid}km```""")
        print(text_weather)
        
    else:
        break 