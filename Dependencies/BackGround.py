from base64 import b64decode
from distutils.ccompiler import gen_lib_options
from json import load, dump
from requests import get
from pymorphy2 import MorphAnalyzer

from datetime import datetime, timedelta

import openai
from gigachat import GigaChat

import Dependencies.Generator as Generator
import Dependencies.Metrics as Mertics

dataFrame_path = "DataWrames/Birthdays.csv"
config_path = 'Configs/config.json'

# Weather
class weather:        
    def GetWeather(sity):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={sity}&units=metric&lang=ru&appid=c38e5a3db7bd33d13d9d0c37f83ccdec"
        weather_data = get(url).json()

        temperature = str(round(weather_data['main']['temp']))
        humidity = str(weather_data['main']['humidity'])
        weathers = str(weather_data['weather'][0]['description'])
        weather_main = str(weather_data['weather'][0]['main'])
        wind = str(weather_data['wind']['speed'])
        wind_deg = weather_data['wind']['deg']
        bar = str(round(weather_data['main']['pressure'] * 0.750062, 1))
        vid = str(weather_data['visibility'] / 1000)

        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = round(wind_deg / 45) % 8
        wind_deg = str(directions[index])
        
        morph = MorphAnalyzer()
        word_c = morph.parse(sity)[0]
        gent = word_c.inflect({'loct'})
        sity = str(gent.word).title()

        weather_split = weathers.split()

        text = " ".join(weather_split[1:len(weather_split)])
        weathers = f"{weather_split[0].title()} {text}"

        weather_text = f"""
    В {sity} сейчас: 
☂ Погода: {weathers} 
℃ Температура: {temperature} °C 
☰ Влажность: {humidity}% 
๑ Ветер: {wind}m/s направление {wind_deg} 
⍗ Давление: {bar}мм.рт.ст 
☁ Видимость: {vid}km"""

        if weather_main == 'Snow':
            snow_speed = weather_data['snow']['1h']
            weather_text = f"{weather_text} \n❄ Скорость снега: {snow_speed} mm/1h"

        return weather_text


    def GetForecast(sity):
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={sity}&units=metric&lang=ru&appid=dfe5e468eadee1e20ded5140d398450c'
        weather_data = get(url).json()

        global_weather = []

        for i in range(len(weather_data['list'])):
            dt = str(weather_data['list'][i]["dt_txt"])

            test = dt.split()

            if test[1] == "12:00:00":
                main_weather = str(weather_data['list'][i]['weather'][0]['description'])
                temperature = str(round(weather_data['list'][i]['main']['temp']))
                humidity = str(weather_data['list'][i]['main']['humidity'])
                wind = str(weather_data['list'][i]['wind']['speed'])
                wind_deg = weather_data['list'][i]['wind']['deg']
                bar = str(round(weather_data['list'][i]['main']['pressure'] * 0.750062, 1))
                vid = str(weather_data['list'][i]['visibility'] / 1000)
                
                directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
                index = round(wind_deg / 45) % 8
                wind_deg = str(directions[index])
                
                weather_split = main_weather.split()
                text = " ".join(weather_split[1:len(weather_split)])
                main_weather = f"{weather_split[0].title()} {text}"

                date = str(weather_data['list'][i]["dt_txt"]).split().pop(0)

                text_weather = (f"""\n{date}:```День: 
☂ Погода: {main_weather.title()}
℃ Температура: {temperature} °C 
☰ Влажность: {humidity}% 
๑ Ветер: {wind}m/s направление {wind_deg} 
⍗ Давление: {bar}мм.рт.ст 
☁ Видимость: {vid}km```""")
                global_weather.append(f"{text_weather}")

            if test[1] == "03:00:00":
                temperature1 = round(weather_data['list'][i]['main']['temp'])
                humidity1 = weather_data['list'][i]['main']['humidity']
                weathers1 = weather_data['list'][i]['weather'][0]['description']
                wind1 = weather_data['list'][i]['wind']['speed']
                wind_deg1 = weather_data['list'][i]['wind']['deg']
                bar1 = round(weather_data['list'][i]['main']['pressure'] * 0.750062, 1)
                vid1 = weather_data['list'][i]['visibility'] / 1000

                directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
                index = round(wind_deg1 / 45) % 8
                wind_deg1 = str(directions[index])
                
                text_weather1 = (f"""```Ночь: 
☂ Погода: {weathers1.title()} 
℃ Температура: {temperature1} °C 
☰ Влажность: {humidity1}% 
๑ Ветер: {wind1}m/s направление {wind_deg1} 
⍗ Давление: {bar1}мм.рт.ст 
☁ Видимость: {vid1}km```""")
                global_weather.append(f"{text_weather1}")

        morph = MorphAnalyzer()
        word_c = morph.parse(sity)[0]
        gent = word_c.inflect({'loct'})
        sity = str(gent.word).title()

        weather_text = f"""
    Прогноз в {sity}:
    {" ".join(global_weather)}"""

        return weather_text


    def GetForecastPerDay(sity):
        sity = "Санкт-петербург"
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={sity}&units=metric&lang=ru&appid=dfe5e468eadee1e20ded5140d398450c'

        weather_data = get(url).json()

        global_weather = []

        for i in range(len(weather_data['list'])):
            if str(weather_data['list'][i]["dt_txt"]).split()[0] == str(datetime.now()).split()[0]:
                main_weather = str(weather_data['list'][i]['weather'][0]['description'])
                temperature = str(round(weather_data['list'][i]['main']['temp']))
                humidity = str(weather_data['list'][i]['main']['humidity'])
                wind = str(weather_data['list'][i]['wind']['speed'])
                wind_deg = weather_data['list'][i]['wind']['deg']
                bar = str(round(weather_data['list'][i]['main']['pressure'] * 0.750062, 1))
                vid = str(weather_data['list'][i]['visibility'] / 1000)
                
                directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
                index = round(wind_deg / 45) % 8
                wind_deg = str(directions[index])
                
                weather_split = main_weather.split()
                text = " ".join(weather_split[1:len(weather_split)])
                main_weather = f"{weather_split[0].title()} {text}"

                date = str(weather_data['list'][i]["dt_txt"]).split().pop(1)

                text_weather = (f"""\n{date}:```День: 
☂ Погода: {main_weather.title()}
℃ Температура: {temperature} °C 
☰ Влажность: {humidity}% 
๑ Ветер: {wind}m/s направление {wind_deg} 
⍗ Давление: {bar}мм.рт.ст 
☁ Видимость: {vid}km```""")

                global_weather.append(text_weather)

            else:
                break 
            
        morph = MorphAnalyzer()
        word_c = morph.parse(sity)[0]
        gent = word_c.inflect({'loct'})
        sity = str(gent.word).title()

        weather_text = f"""
    Прогноз в {sity}:
    {" ".join(global_weather)}"""

        return weather_text


    def create_temp_metric(sity):
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={sity}&units=metric&lang=ru&appid=dfe5e468eadee1e20ded5140d398450c'
        weather_data = get(url).json()

        dates = []
        temps = []

        for i in range(len(weather_data['list'])):
            dt = str(weather_data['list'][i]["dt_txt"])

            test = dt.split()

            if test[1] == "15:00:00":
                dates.append(str(weather_data["list"][i]["dt_txt"]).split()[0])
                temps.append(int(weather_data["list"][i]['main']['temp']))

        data_json = {
            'date': dates,
            'temperature': temps
        }

        path = f"{Mertics.create_temp_metric(data_json)}"

        with open(path, "rb") as metrics:
            write_data = metrics.read()

            metrics.close()

        return write_data


class add:
    def checkCanceled(text):
        if text == "Отмена" or text == 'отмена':
            return True


    def addNewUser(message, onCommand=False):
        try:
            argus = message.text.split()
            # if onCommand(): argus.pop(0)

            if len(argus) < 4:
                return "❌Укажите данные в полном объеме. Попробуйте снова."

            if (str(argus[2]).count("0") != 0) | (str(argus[3]).count("0") != 0):
                return "❌Я же сказал без нулей. Попробуйте снова."

            if int(argus[2]) < 1 or int(argus[3]) < 1 or int(argus[2]) > 31 or int(argus[3]) > 12:
                return "❌Такой даты не существует. Попробуйте снова."

            morph = MorphAnalyzer()
            word_c = morph.parse(argus[0])[0]
            gent = word_c.inflect({'datv'})

            save_text = f"{str(gent.word).title()},@{message.from_user.username},{argus[2]},{argus[3]}"

            with open(dataFrame_path, 'a') as f:
                f.write(save_text + '\n')
                f.close()

            return True

        except Exception as e:
            return False
   
    
class config:
    def loadConfig():
        with open(config_path) as file_data:
            data = load(file_data)
            base_model = data["base_model"]
            technical_brake = data['technical_brake']
            ask_q = data["ask_q"]
            gen_q = data["gen_q"]
            file_data.close()

            return base_model, technical_brake, ask_q, gen_q


    def pushConfig(tech_brake, ask_q, gen_q):
        with open(config_path, "r") as file_data:
            data = load(file_data)
            data["technical_brake"] = tech_brake
            data["ask_q"] = ask_q
            data["gen_q"] = gen_q
            # data["global_time_work"] = global_time_work

            with open(config_path, "w") as file_data:
                dump(data, file_data, ensure_ascii=False, indent=4)
                file_data.close()
            file_data.close()

        return True
    

class ask:
    def askGC(promt, token):
        with GigaChat(credentials=token, verify_ssl_certs=False) as giga:
            answer_text = giga.chat(promt).choices[0].message.content    

        answer_text = f"GigaChat - {answer_text}"

        return answer_text 

    # Ask
    def askGPT(promt, model, token):
        print(model)
        openai.api_key = token
        completion = openai.ChatCompletion.create(
        model=str(model),
      messages=[
        {"role": "user", "content": promt}
      ]
    )
        answer_text = completion.choices[0].message.content
        answer_text = f"{model} - {answer_text}"

        return answer_text
    
    
class gen:
    def GetKandiskyModel():
        api = Generator.Text2ImageAPI('https://api-key.fusionbrain.ai/', '1501B6B5F8996BCE2B0D4E0DAAC0E721', '5C015D1AC4CBB006B3375E00B821A138')
        return api.get_model()


    def ImageGenerator(promt):
        api = Generator.Text2ImageAPI('https://api-key.fusionbrain.ai/', '1501B6B5F8996BCE2B0D4E0DAAC0E721', '5C015D1AC4CBB006B3375E00B821A138')
        model_id = api.get_model()
        uuid = api.generate(promt, model=model_id)
        images = api.check_generation(uuid)

        return images


    def CheckCensored(images):
        if images['censored'] != None:
            if images['censored'] == True:
                return True
        return False


    def ConvertImage(image):
        return b64decode(image)


    def CheckLenImages(images):
        if len(images) < 0: return True
        else: return False


    def GetSummorysenNumber(message):
        command_split = message.text.split()
        command_split.pop(0)

        if (len(command_split) < 1) | (command_split[0] != int): summorysen_coll = 350
        else: summorysen_coll = int(command_split[0])

        return summorysen_coll


class summoryzen:
    def CheckSumNumberInRange(sum_coll):
        if sum_coll not in [50, 100, 150, 350]: return True
        else: return False
 

    def GetLines(summorysen_coll):
        lines = []

        with open("history.txt", 'r') as history:
            for line in history:
                lines.append(line.strip())
            history.close()

        get_text = " ".join(lines[(len(lines) - summorysen_coll):len(lines)])

        return get_text
    
# Profile
class Tokens:
    
    def GetLastTokens(message, use_tokens, last_token):
        ms_text = f"""
Потраченно ⊚: {use_tokens} 
Осталось ⊚: {last_token}"""
        return ms_text
    
    def GetLastImages(message, last_image):
        ms_text = f"""
Осталось ⊚: {last_image}"""
        return ms_text 


class logs:
    def clearLogs():
        with open("logs/logs.log", "w") as history:
            history.write("\n")
            history.close()


    def get_logs(q_str):
        lines = []

        with open("logs/logs.log", "r") as history: 
            for line in history:
                lines.append(f"{line.strip()} \n")
            history.close()

        if len(lines) < q_str:
            return "❌Недостаточно логов!"

        get_text = " ".join(lines[(len(lines) - q_str):len(lines)])

        return get_text
    
    
def markdown_convert(text):
    if True:
        fix_txt = []
        for i in text:
            if i in ['_', "*", ">", "<", '-', '.', ',', '{', '}', '(', ')', '+', '#', "!", '=']:
                fix_txt.append("\\")
                fix_txt.append(i)
            else:
                fix_txt.append(i)

        text = "".join(fix_txt)
        
        return text
    else:
        return text  
    
    
def mathToken(text, is_gpt4 = False):
    use_tokens = len(text)
    
    if is_gpt4: use_tokens * 2
    
    return use_tokens


def chenkChatType(message):
    if str(message.chat.type) == 'private':
        return False
    else:
        return True


def checkPromt(text):
    argus = str(text).split()
    if len(argus) > 2: return False 
    else:
        return True
    
     
def getPromt(text):
    argus = str(text).split()
    argus.pop(0)
    
    text = " ".join(argus)
    
    return text


def freshcheck(message, fr_time):
    time_difference = datetime.now() - datetime.fromtimestamp(message.date)
    print(time_difference)
    if time_difference > timedelta(minutes=fr_time):
        return True
    else:
        return False