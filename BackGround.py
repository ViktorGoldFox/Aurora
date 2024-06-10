from base64 import b64decode
from json import load
from h11 import Data
from requests import get
from pymorphy2 import MorphAnalyzer

from datetime import datetime, timedelta

import openai
from gigachat import GigaChat

import DataBase
import Generator

# Weather
def GetWeather(sity):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={sity}&units=metric&lang=ru&appid=c38e5a3db7bd33d13d9d0c37f83ccdec"
    weather_data = get(url).json()
    
    temperature = str(round(weather_data['main']['temp']))
    humidity = str(weather_data['main']['humidity'])
    weathers = str(weather_data['weather'][0]['description'])
    weather_main = str(weather_data['weather'][0]['main'])
    wind = str(weather_data['wind']['speed'])
    bar = str(round(weather_data['main']['pressure'] * 0.750062, 1))
    vid = str(weather_data['visibility'] / 1000)
    
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
    ๑ Ветер: {wind}m/s 
    ⍗ Давление: {bar}мм.рт.ст 
    ☁ Видимость: {vid}km"""
    
    if weather_main == 'Snow':
        snow_speed = weather_data['snow']['1h']
        weather_text = f"{weather_text} \n❄ Скорость снега: {snow_speed} mm/1h"
        
    return weather_text
    
    
def checkCanceled(text):
    if text == "Отмена" or text == 'отмена':
        return True


def checkCurNickName(message): DataBase.check.CurentNickname(message)


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
        
        with open('DateFrame.csv ', 'a') as f:
            f.write(save_text + '\n')
            f.close()
        
        return True
        
    except Exception as e:
        return False
    
      
def loadConfig():
    with open("config.json") as file_data:
        data = load(file_data)
        base_model = data["base_model"]
        technical_brake = data['technical_brake']
        ask_q = data["ask_q"]
        gen_q = data["gen_q"]
        file_data.close()
        
        return base_model, technical_brake, ask_q, gen_q
    
    
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
    if time_difference > timedelta(minutes=fr_time):
        return True
    else:
        return False
    

def NotAvailabilityUser(message, gp_id, user_status):
    if message.chat.id != gp_id:
        DataBase.check.add_user(message, user_status)
    

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
    
    
# Generate
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
def get_profile(message, user_status):
    return DataBase.get_profile(message, member_status=user_status)

# Tokens
def CheckShowLastToken(message, gp_id):
    return DataBase.check.ShowLastToken(message.chat.id, gp_id)


def GetLastTokens(message, use_tokens):
    ms_text = f"""
Потраченно ⊚: {use_tokens} 
Осталось ⊚: {DataBase.get_last_tokens(message)}"""
    return ms_text


def GetCurrentModel(message): return DataBase.getCurrentModel(message)


def GetLastImages(message):
    ms_text = f"""
Осталось ⊚: {DataBase.get_last_images(message)}"""
    return ms_text

def CheckTokenAsk(message, use_token): return DataBase.check.tokens_ask(message, use_token)


def CheckTokenGen(message): return DataBase.check.tokens_gen(message)


def GetModel(message): return DataBase.getCurrentModel(message)

def GetModels(message): return DataBase.get_models(message.chat.id)

def changeModel(message, model): DataBase.changeModel(message, model)


def mathToken(text, is_gpt4 = False):
    use_tokens = len(text)
    
    if is_gpt4: use_tokens * 2
    
    return use_tokens

def checkTokens(message, use_tokens):
    if DataBase.check.tokens_ask(message, use_tokens): return "❌Недостаточно токенов! Для покупки писать сюда - @ViktorGoldFox"