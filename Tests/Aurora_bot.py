 #-=-=-=-=-=-=-=-=-=-=-=-
#Создатель:ViktorGoldFox
#-=-=-=-=-=-=-=-=-=-=-=-
#Aurora bot
from shlex import join
from site import check_enableusersite
from time import sleep 
import telebot
import pandas as pd
import schedule
import datetime
from datetime import timedelta
import threading
from urllib import request 
import requests 
import pymorphy2
import openai
from translate import Translator
import base64
from telebot import types
from logzero import logger, logfile
import Generator
import DataBase
from gigachat import GigaChat

logfile("logs.log")

tex_stat = False
version = 'v5'

donate_url = 'https://boosty.to/vitusik_kentusik.org/donate'
#OpenAi
openai.api_key = "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"
request_gpt_coll = 0
request_gpt_rekl = 0

Gigachat_token = 'Y2Q4ZmU4YWEtOWE5OS00OGU4LWExNjEtM2U2YWE2Y2NlYzYwOjQzNzI4YjE4LWM1YzAtNDIzYy1iZTA0LWE2OTE1YjE5Yzc3Zg=='
request_gen_rekl = 0
request_gen_coll = 0

AIlimit = 50
Animspeed = 0.03
Text_limit = 800

# translator= Translator(from_lang="Russian",to_lang="English")

#Указание сайта погоды (Open wheather)
url = 'https://api.openweathermap.org/data/2.5/weather?q=Saint%20Petersburg&units=metric&lang=ru&appid=c38e5a3db7bd33d13d9d0c37f83ccdec'

#Бот конфиг 
chatid = '-1001665880322'
token = '6904577368:AAHMjsneMF0HaLHiWa08Bv2ZzBZOwIJ7yTo'
# token = '6717661703:AAHP8jd6rYcVRei-4nJ2Satsq1E5aTtIKFA'

bot = telebot.TeleBot(token=token)
    
#Указание админов
admins = [1746901164, 1018366370]
push_message_admin = [admins[0]]
data = pd.read_csv("DateFrame.csv")

#Указание переменных
NowDR = []
start_time = datetime.datetime.now()
NowDate = datetime.datetime.now()
time = NowDate.replace(microsecond=0)

#Установка времени
Weather_time = "08:00"
Gift_time = "10:00"
#Обработка команнд
@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, "/ask Вопрос - Задать вопрос chatGPT \n /add - Добавиться в базу данных \n /weather - Вывести погоду \n/weather ГОРОД- Вывести погоду в городе \n /forecast - Вывести прогноз погоды \n /generate Описание картины \n Version: " + version)
@bot.message_handler(commands=['start'])
def show_start(message):
    bot.send_message(message.chat.id, f'Привет! Я - нейросетевой бот AuroraBot {version}, и я здесь, чтобы повеселиться. Я могу помочь тебе в разных задачах /help. Я люблю общаться с людьми и узнавать что-то новое. Давай пообщаемся!')
@bot.message_handler(commands=['add'])
def appending(message):
    if str(message.chat.type) != 'private':
        bot.send_message(message.chat.id, "❌Напиши команду боту в личные сообщения")
        error_mess
        sleep(5)
        bot.delete_message(message.chat.id, message_id=error_mess.message_id)
        return False
    if bot.get_chat_member(chatid, message.from_user.id).status == 'left':
        error_mess = bot.send_message(message.chat.id, "❌Вы не являетесь участником группы.")
        error_mess
        sleep(5)
        bot.delete_message(message.chat.id, message_id=error_mess.message_id)
        return False
    bot.send_message(message.from_user.id, "Отправь данные без нулей через пробелы в формате: Name Day Month. Пример: Виктор 19 1. Если хотите отменить запись введите: Отмена")
    log("Добавлен новый пользователь!")
    bot.register_next_step_handler(message,save_new)
@bot.message_handler(commands=['report'])
def report(message):
    argus = message.text.split()
    if len(argus) < 2:
        error = bot.send_message(message.chat.id, "После комманды нужно описать проблему/пожелания. Попробуй снова.")
        error
        sleep(5)
        bot.delete_message(message.chat.id, message_id=error.message_id)
        return False
    argus.pop(0)
    report_text = " ".join(argus)
    log = f"@{message.from_user.username} отправил репорт: {report_text}"
    logger.debug(f"Отправили репорт тест: {log}")
    bot.send_message(admins[0], str(log))
#==========================================================
@bot.message_handler(commands=['sum'])
def get_last_messages(message):
    try:
        time_difference = datetime.datetime.now() - datetime.datetime.fromtimestamp(message.date)
        if time_difference > timedelta(minutes=5):
            bot.send_message(message.chat.id, str("❌Запрос устарел. Попробуйте снова!"))
            return True
        if tex_stat:
            if message.chat.id not in admins:
                bot.send_message(message.chat.id, '❌Идут тех. работы! Попробуйте позже!')
                return False
        if bot.get_chat_member(chatid, message.from_user.id).status == 'left':
            error_mess = bot.send_message(message.chat.id, "❌Вы не являетесь участником группы.")
            error_mess
            sleep(5)
            bot.delete_message(message.chat.id, message_id=error_mess.message_id)
            bot.delete_message(message.chat.id, message_id=message.message_id)
            return False
        if str(message.chat.id) != chatid:
            error_mess = bot.send_message(message.chat.id, "❌Пропишите комманду в группе.")
            error_mess
            sleep(5)
            bot.delete_message(message.chat.id, message_id=error_mess.message_id)
            bot.delete_message(message.chat.id, message_id=message.message_id)
            return False
        
        bot.send_message(message.chat.id, "❌Эта функция временно не доступна.")
        return False
    
        command = message.text.split()
        if len(command) < 2:
            summorysen_coll = 350
        command.pop(0)
        summorysen_coll = int(command[0])
        if summorysen_coll not in [50, 100, 150, 300]:
            error_mess = bot.send_message(message.chat.id,"❌Значения для суммирования: 50,100,150,350. Попробуйте снова.")
            error_mess
            sleep(5)
            bot.delete_message(message.chat.id, message_id=error_mess.message_id)
            bot.delete_message(message.chat.id, message_id=message.message_id)
            return False
        mess_anim = bot.send_message(message.chat.id, "🕐Ваш запрос обрабатывается, это может занять несколько минут...")
        mess_anim
        common_lines = []
        with open("history.txt", 'r') as file:
            for line in file:
                common_lines.append(line.strip())
        file.close()
        get_text = " ".join(common_lines[(len(common_lines) - summorysen_coll):len(common_lines)])
        promt = f'Суммируй эти сообщения обязательно с упоминанием пользователей и что они писали кратко и обрабатывая каждое сообщение не списком а целым текстом без общей темы в конце и с капелькой дичи объем: 0.5 страниц: {get_text}'
        if summorysen_coll <= 100:
            promt = f'Суммируй эти сообщения обязательно с упоминанием пользователей и что они писали обрабатывая каждое сообщение не списком а целым текстом без общей темы в концеи с капелькой дичи  объем: 1 страниц: {get_text}'
        if summorysen_coll >= 150:
            promt = f'Суммируй эти сообщения обязательно с упоминанием пользователей и что они писали обрабатывая каждое сообщение не списком а целым текстом без общей темы в конце и с капелькой дичи  очееень длинно и развернуто в 10 страниц: {get_text}'
        completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0125",
  messages=[
    {"role": "user", "content": promt}
  ]
)
        complet_text = completion.choices[0].message.content
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("❤️Поддержать автора", url=donate_url)
        markup.add(btn)
        complet_text = str(f"Aurora-{version} - Последние {summorysen_coll} cообщений суммированны так: \n{complet_text}")
        
        bot.edit_message_text(chat_id=message.chat.id,message_id=mess_anim.message_id,text=complet_text)
        # bot.send_message(message.chat.id,complet_text, reply_markup=markup)
        # bot.delete_message(message.chat.id, message_id=mess_anim.message_id)
        logger.info(f'@{message.from_user.username} суммировал {summorysen_coll} сообщений')
        log(f'@{message.from_user.username} суммировал {summorysen_coll} сообщений')
    except Exception as e:
        log("Error")
        logger.error(f' Summory text error. Code: {e}')
        return False
#=====================================================================
@bot.message_handler(commands=['generate', 'gen'])
def generate_image(message):
    global request_gen_coll
    global request_gen_rekl
    # try:
    if True:
        mess = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше изображение обрабатывается...")
        mess
        time_difference = datetime.datetime.now() - datetime.datetime.fromtimestamp(message.date)
        if time_difference > timedelta(minutes=5):
            # bot.send_message(message.chat.id, str("❌Запрос устарел. Попробуйте снова!"))
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Запрос устарел. Попробуйте снова!")
            return True
        
        if message.from_user.username == None:
            # error_mess = bot.send_message(message.chat.id, "❌Прежде чем использовать комманду generate, надо установить никнейм!")
            # error_mess
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Прежде чем использовать комманду generate, надо установить никнейм!")
            sleep(5)
            bot.delete_message(message.chat.id, message_id=mess.message_id)
            bot.delete_message(message.chat.id, message_id=message.message_id)
            return False
            
        if (tex_stat) & (message.chat.id not in admins): 
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Идут тех. работы! Попробуйте позже!")
            # bot.send_message(message.chat.id, '❌Идут тех. работы! Попробуйте позже!')
            return False
        
        time_start = datetime.datetime.now()
        time_start = time_start.replace(microsecond=0)
        
        argus = message.text.split()
        
        if len(argus) < 2:
            # error_mess = bot.send_message(message.chat.id, "❌Нужно ввести запрос.Попробуйте снова!")
            # error_mess
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Нужно ввести запрос.Попробуйте снова!")
            sleep(5)
            bot.delete_message(message.chat.id, message_id=mess.message_id)
            bot.delete_message(message.chat.id, message_id=message.message_id)
            return False
        
        argus.pop(0)
        promt = " ".join(argus)
        
        use_tokens = 0
        for i in promt:
            use_tokens+=1
        use_tokens = use_tokens * 5
        
        result = DataBase.check.subscribe(message, bot.get_chat_member(-1002064516590, message.from_user.id).status)
        match result:
            case 401:
                bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Для начала работы с нейросетями подпишитесь на канал @Aurorafloodbot_info, и повторите попытку")
                # bot.send_message(message.chat.id, "Для начала работы с нейросетями подпишитесь на канал @Aurorafloodbot_info, и повторите попытку")
                logger.info(f"@{message.from_user.nickname} code: {result}")
                return result
            
        result = DataBase.check.tokens_gen(message, use_tokens)
        match result:
            case 402:
                # bot.send_message(message.chat.id, "❌Недостаточно токенов! Для покупки писать сюда - @ViktorGoldFox")
                bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Недостаточно токенов! Для покупки писать сюда - @ViktorGoldFox")
                logger.info(f"@{message.from_user.nickname} code: {result}")
                return result
            case 1:
                DataBase.check.data(message, bot.get_chat_member(chatid, message.from_user.id).status)
        
        api = Generator.Text2ImageAPI('https://api-key.fusionbrain.ai/', '1501B6B5F8996BCE2B0D4E0DAAC0E721', '5C015D1AC4CBB006B3375E00B821A138')
        model_id = api.get_model()
        uuid = api.generate(promt, model=model_id)
        images = api.check_generation(uuid)
        
        if len(images) < 0:
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Генерация временно недоступна. Обратитесь к администратору.")
            #  bot.send_message(message.chat.id, '❌Генерация временно недоступна. Обратитесь к администратору.')
        
        if images['censored'] != None:
            if images['censored'] == True:
                # bot.send_message(message.chat.id, '❌Промт зацензурен. Генерация невозможна')
                bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text='❌Промт зацензурен. Генерация невозможна')
                return False
        
        
        time_end = datetime.datetime.now()
        time_end = time_end.replace(microsecond=0)
        complet_time = time_end - time_start
        
        request_gen_rekl+=1
        request_gen_coll += 1
        
        logger.info(f"@{message.from_user.username} Сгенерировал изображение: {promt} Время гена: {complet_time}")
        
        log(f"@{message.from_user.username} Сгенерировал изображение: {promt}")
        
        image_base64 = images['images'][0] 
        image_data = base64.b64decode(image_base64)
        image_name = f'image-'+str(time_end)+'.png'
        
        result = DataBase.give_tokens.gen(message, use_tokens)
                    
        # with open(f'"logs/{image_name}"', "wb") as file:
        #     file.write(image_data)
        #     file.close()
        
        # with open(f'"logs/{image_name}"', 'rb') as im:
        if True:
            im = image_data
            if request_gen_rekl == 5:
                request_gen_rekl = 0
                
                markup = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton("❤️Поддержать автора", url=donate_url)
                markup.add(btn)
                
                if (str(message.chat.id) != chatid):
                    
                    datauser = pd.read_csv("user.csv")
                    index = datauser.index[datauser['chat_id'] == message.chat.id][0]
                    last_tokens = datauser.loc[index, "tokens"]
                    
                    if str(datauser.loc[index, "status"]) not in ['admin', 'mvp', 'group']:
                        bot.send_photo(message.chat.id, im, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово за " + str(complet_time) + f"\nПотраченно токенов: {use_tokens} \nОсталось: {last_tokens}"), reply_markup=markup)
                    else:
                        bot.send_photo(message.chat.id, im, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово за " + str(complet_time)), reply_markup=markup)
                else:
                    bot.send_photo(message.chat.id, im, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово за " + str(complet_time)), reply_markup=markup)
            else:
                if (str(message.chat.id) != chatid):
                    
                    datauser = pd.read_csv("user.csv")
                    index = datauser.index[datauser['chat_id'] == message.chat.id][0]
                    
                    if str(datauser.loc[index, "status"]) not in ['admin', 'mvp', 'group']:
                        last_tokens = datauser.loc[index, "tokens"]
                        bot.send_photo(message.chat.id, im, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово за " + str(complet_time) + f"\nПотраченно токенов: {use_tokens} \nОсталось: {last_tokens}"))
                    else:
                        bot.send_photo(message.chat.id, im, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово за " + str(complet_time)))
                else:
                    bot.send_photo(message.chat.id, im, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово за " + str(complet_time)))
            # im.close()
        bot.delete_message(message.chat.id, message_id=mess.message_id)
    # except Exception as e:
    #     log("Error")
    #     bot.send_message(message.chat.id, '❌Генерация временно недоступна. Обратитесь к администратору.')
    #     logger.error(f'Image generate. code: {e}')
    #     return False

        
#=========================================================
#Вопросы chat-gpt
@bot.message_handler(commands=['ask'])
def ask_chatgpt(message, chat_state = True):
    global request_gpt_coll
    global request_gpt_rekl
    # try:
    if True:
        mess = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше сообщение обрабатывается")
        mess
        time_difference = datetime.datetime.now() - datetime.datetime.fromtimestamp(message.date)
        if time_difference > timedelta(minutes=5):
            # bot.send_message(message.chat.id, str("❌Запрос устарел. Попробуйте снова!"))
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Запрос устарел. Попробуйте снова!")
            return True
        
        if message.from_user.username == None:
            # error_mess = bot.send_message(message.chat.id, "❌Прежде чем использовать комманду ask, надо установить никнейм!")
            # error_mess
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Прежде чем использовать комманду ask, надо установить никнейм!")
            sleep(5)
            bot.delete_message(message.chat.id, message_id=mess.message_id)
            bot.delete_message(message.chat.id, message_id=message.message_id)
            return False
        # if (datetime.datetime.fromtimestamp()
        if (tex_stat) & (message.chat.id not in admins):
            # bot.send_message(message.chat.id, '❌Идут тех. работы! Попробуйте позже!')
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Идут тех. работы! Попробуйте позже!")
            return False
        
        time_start = datetime.datetime.now()
        time_start = time_start.replace(microsecond=0)
        
        # argus = message.text.split()
        # if len(argus) < 2:
        #     error_mess = bot.send_message(message.chat.id, "❌Нужно ввести запрос.Попробуйте снова!")
        #     error_mess
        #     sleep(5)
        #     bot.delete_message(message.chat.id, message_id=error_mess.message_id)
        #     return False
        
        if chat_state:
            argus = message.text.split()
            if len(argus) < 2:
                # error_mess = bot.send_message(message.chat.id, "❌Нужно ввести запрос.Попробуйте снова!")
                # error_mess
                bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Нужно ввести запрос.Попробуйте снова!")
                sleep(5)
                bot.delete_message(message.chat.id, message_id=mess.message_id)
                return False
            argus.pop(0)
            promt = " ".join(argus)
        else:
            promt = message.text
            
        if message.reply_to_message != None:
            promt = f"{promt}: {message.reply_to_message.text}"
        # argus.pop(0)
        # promt = " ".join(argus)
        
        use_tokens = 0
        for i in promt:
            use_tokens+=1
            
        result = DataBase.check.subscribe(message, bot.get_chat_member(-1002064516590, message.from_user.id).status)
        match result:
            case 401:
                bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Для начала работы с нейросетями подпишитесь на канал @Aurorafloodbot_info, и повторите попытку")
                # bot.send_message(message.chat.id, "Для начала работы с нейросетями подпишитесь на канал @Aurorafloodbot_info, и повторите попытку")
                # logger.info(f"@{message.from_user.nickname} code: {result}")
                return result
            
        result = DataBase.check.tokens_ask(message, use_tokens)
        match result:
            case 402:
                # bot.send_message(message.chat.id, "❌Недостаточно токенов! Для покупки писать сюда - @ViktorGoldFox")
                bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text="❌Недостаточно токенов! Для покупки писать сюда - @ViktorGoldFox")
                # logger.info(f"@{message.from_user.nickname} code: {result}")
                return result
            case 1:
                DataBase.check.data(message, bot.get_chat_member(chatid, message.from_user.id).status)
            
        DataBase.give_tokens.ask(message, use_tokens)
#         completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo-16k-0613",
#   messages=[
#     {"role": "user", "content": promt}
#   ]
# )
        with GigaChat(credentials=Gigachat_token, verify_ssl_certs=False) as giga:
            response = giga.chat(promt)

        response = response.choices[0].message.content

        # text = str("ChatGPT - " + completion.choices[0].message.content)
        # text = str("ChatGPT - " + response)
        text = str("GigaChat - " + response)
        
        time_end = datetime.datetime.now()
        time_end = time_end.replace(microsecond=0)
        complet_time = time_end - time_start
        
        bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text=f"✅Ваш запрос обработан за {complet_time}")
    
        logger.info(f"@{message.from_user.username} Воспользовался ChatGPT:{promt} Время ответа: {complet_time} Ответ: {text}")
        log(f"@{message.from_user.username} Воспользовался ChatGPT:{promt}")
        request_gpt_coll+=1
        request_gpt_rekl+=1
        index = 0
        fix_txt = []
        for i in text:
            if i in ['_', "*", ">", "<", '-', '.', ',', '{', '}', '(', ')', '+', '#', "!", '=']:
                fix_txt.append("\\")
                fix_txt.append(i)
            else:
                fix_txt.append(i)
        text = "".join(fix_txt)
        if request_gpt_rekl == 7:
            request_gpt_rekl = 0
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("❤️Поддержать автора", url=donate_url)
            markup.add(btn)
            bot.send_message(message.chat.id,f"""{text}""", reply_markup=markup, parse_mode='MarkdownV2')
            return False
        argus = text.split()
        if len(argus) > Text_limit:
            txt_one = " ".join(argus[:Text_limit])
            txt_two = " ".join(argus[Text_limit:])
            bot.send_message(message.chat.id, f"""{text}""", parse_mode='MarkdownV2')
            bot.send_message(message.chat.id, txt_two, parse_mode="MarkdownV2")
            return False
        if str(message.chat.id) != chatid: 
            datauser = pd.read_csv("user.csv")
            index = datauser.index[datauser['chat_id'] == message.chat.id][0]
            if (str(datauser.loc[index, 'status']) not in ['admin', 'mvp', 'group']):
                index = datauser.index[datauser['chat_id'] == message.chat.id][0]
                last_tokens = datauser.loc[index, "tokens"]
                bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text=f"""{text} \nПотраченно токенов: {use_tokens} \nОсталось: {last_tokens}""", parse_mode="MarkdownV2")
                # bot.send_message(message.chat.id, f"""{text} \nПотраченно токенов: {use_tokens} \nОсталось: {last_tokens}""", parse_mode='MarkdownV2')
            else:
                bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text=f"""{text}""", parse_mode='MarkdownV2')
                # bot.send_message(message.chat.id, f"""{text}""", parse_mode='MarkdownV2')
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=mess.message_id, text=f"""{text}""", parse_mode='MarkdownV2')
            
        # bot.delete_message(message.chat.id, message_id=mess.message_id)
    # except Exception as e:
    #     logger.error(f'Chat error. Code: {e}')
    #     log("Error")
    #     bot.send_message(message.chat.id, 'ChatGPT времмено недоступен! Попробуйте позже.')
#========================================================= 
#Обработка команнд
@bot.message_handler(commands=['weather'])
def send_weather_person(message):
    try:
        argus = message.text.split()
        siti = 'Санкт-петербург'
        url = 'https://api.openweathermap.org/data/2.5/weather?q=Saint%20Petersburg&units=metric&lang=ru&appid=c38e5a3db7bd33d13d9d0c37f83ccdec'
        if len(argus) > 1:
            argus.pop(0)
            siti = ''.join(argus)
            url = f'https://api.openweathermap.org/data/2.5/weather?q={siti}&units=metric&lang=ru&appid=c38e5a3db7bd33d13d9d0c37f83ccdec'
        weather_data = requests.get(url).json()
        temperature = str(round(weather_data['main']['temp']))
        humidity = str(weather_data['main']['humidity'])
        weathers = str(weather_data['weather'][0]['description'])
        weather_main = str(weather_data['weather'][0]['main'])
        wind = str(weather_data['wind']['speed'])
        bar = str(round(weather_data['main']['pressure'] * 0.750062, 1))
        vid = str(weather_data['visibility'] / 1000)
        morph = pymorphy2.MorphAnalyzer()
        word_c = morph.parse(siti)[0]
        gent = word_c.inflect({'loct'})
        siti = str(gent.word).title()
        text = (f"В {siti} сейчас: \nПогода: {weathers.title()} \nТемпература: {temperature} °C \nВлажность: {humidity}% \nВетер: {wind}m/s \nДавление: {bar}мм.рт.ст \nВидимость: {vid}km")
        if weather_main == 'Snow':
            snow_coll = weather_data['snow']['1h']
            text = (f"В {siti} сейчас: \nПогода: {weathers.title()} \nТемпература: {temperature} °C \nВлажность: {humidity}% \nВетер: {wind}m/s \nДавление: {bar}мм.рт.ст \nВидимость: {vid}km \nСкорость снега: {snow_coll}mm/1h")
        logger.info(f'Выведенна погода пользователю: {message.from_user.username}')
        log(f'Выведенна погода пользователю: {message.from_user.username}')
        bot.send_message(message.chat.id,text)   
    except Exception as e:
        logger.error(f"Ошибка в погоде: {e}") 
        error_mess = bot.send_message(message.chat.id, 'В названии города ошибка. Попробуйте снова!')
        error_mess
        sleep(5)
        bot.delete_message(message.chat.id, message_id=error_mess.message_id)
        bot.delete_message(message.chat.id, message_id=message.message_id)
        return False
#==========================================================
@bot.message_handler(commands=['forecast'])
def send_weather_person(message):
    try:
        argus = message.text.split()
        siti = 'Санкт-петербург'
        url = 'http://api.openweathermap.org/data/2.5/forecast?q=Saint%20Petersburg&units=metric&lang=ru&appid=dfe5e468eadee1e20ded5140d398450c'
        if len(argus) > 1:
            argus.pop(0)
            siti = ''.join(argus)
            url = f'http://api.openweathermap.org/data/2.5/forecast?q={siti}&units=metric&lang=ru&appid=dfe5e468eadee1e20ded5140d398450c'
        weather_data = requests.get(url).json()
        global_weather = []
        for i in range(len(weather_data['list'])):
            dt = str(weather_data['list'][i]["dt_txt"])
            test = dt.split()
            dt = dt.replace("-", '\.')
            if test[1] == "12:00:00":
                temperature = str(round(weather_data['list'][i]['main']['temp']))
                humidity = str(weather_data['list'][i]['main']['humidity'])
                weathers = str(weather_data['list'][i]['weather'][0]['description'])
                weather_main = str(weather_data['list'][i]['weather'][0]['main'])
                wind = str(weather_data['list'][i]['wind']['speed'])
                bar = str(round(weather_data['list'][i]['main']['pressure'] * 0.750062, 1))
                vid = str(weather_data['list'][i]['visibility'] / 1000)
                morph = pymorphy2.MorphAnalyzer()
                word_c = morph.parse(siti)[0]
                gent = word_c.inflect({'loct'})
                siti = str(gent.word).title()
                date = str(test[0]).replace("-", '\.')
                text_weather = (f"""\n{date}:```День: \nПогода: {weathers.title()} \nТемпература: {temperature} °C \nВлажность: {humidity}% \nВетер: {wind}m/s \nДавление: {bar}мм.рт.ст \nВидимость: {vid}km```""")
                global_weather.append(f"{text_weather}")
            if test[1] == "03:00:00":
                temperature1 = str(round(weather_data['list'][i]['main']['temp']))
                humidity1 = str(weather_data['list'][i]['main']['humidity'])
                weathers1 = str(weather_data['list'][i]['weather'][0]['description'])
                weather_main1 = str(weather_data['list'][i]['weather'][0]['main'])
                wind1 = str(weather_data['list'][i]['wind']['speed'])
                bar1 = str(round(weather_data['list'][i]['main']['pressure'] * 0.750062, 1))
                vid1 = str(weather_data['list'][i]['visibility'] / 1000)
                morph = pymorphy2.MorphAnalyzer()
                word_c = morph.parse(siti)[0]
                gent1 = word_c.inflect({'loct'})
                siti = str(gent1.word).title()
                text_weather1 = (f"""```Ночь: \nПогода: {weathers1.title()} \nТемпература: {temperature1} °C \nВлажность: {humidity1}% \nВетер: {wind1}m/s \nДавление: {bar1}мм.рт.ст \nВидимость: {vid1}km```""")
                global_weather.append(f"{text_weather1}")
        text = " ".join(global_weather)
        bot.send_message(message.chat.id,f"{text}", parse_mode="MarkdownV2")
        logger.info(f'Выведен прогноз погоды пользователю: {message.from_user.username}')
        log(f'Выведен прогноз погоды пользователю: {message.from_user.username}')
    except Exception as e:
        error_mess = bot.send_message(message.chat.id, '❌В названии города ошибка. Попробуйте снова!')
        error_mess
        sleep(5)
        bot.delete_message(message.chat.id, message_id=error_mess.message_id)
        bot.delete_message(message.chat.id, message_id=message.message_id)
        return False
#----------------------------------------------------------         
@bot.message_handler(commands=['profile'])
def profile(message): 
    if str(message.chat.type) != 'private':
        bot.send_message(message.chat.id, "❌Напиши команду боту в личные сообщения")
        return False
    datauser = pd.read_csv("user.csv")
    if datauser[datauser['chat_id'] == message.chat.id].shape[0] == 0:
        if bot.get_chat_member(chatid, message.from_user.id).status == 'left':
            append_data = f"{message.from_user.username},{message.chat.id},default,250"
        else:
            append_data = f"{message.from_user.username},{message.chat.id},group,0"
        with open("user.csv", 'a') as csv:
            csv.write(f"\n{append_data}")
            csv.close()
        logger.debug("Add new user")
    datauser = pd.read_csv("user.csv")
    index = datauser.index[datauser['chat_id'] == message.chat.id][0]
    name = datauser.loc[index, "name"]
    status = datauser.loc[index, "status"]
    if str(status) in ['admin', 'mvp', 'group']:
        tokens = '∞'
    else:
        tokens = datauser.loc[index, "tokens"]
    form = f"""
    ⭐️Профиль
        📕Имя: {name}
        📖Статус: {status}
        💲Токены: {tokens}
    """
    bot.send_message(message.chat.id, form, parse_mode="MarkdownV2")
#----------------------------------------------------------
@bot.message_handler(commands=['promo'])
def prom(message):
    if len(message.text.split()) < 2:
        bot.send_message(message.chat.id, 'Введи промо после комманды')
        return False
    # if message.text.split()[1] in ["8G3H5E7J6K", "X9Z7K1D3C8", "L6M2N9B1V5", "P4O6I8U7Y2","Q1W5E9R4T7","H3J7K6L0P9", "V2B4N1M8X3","Z7X9Y2C6V1", "R4T5Y7U2I8"]:
    datauser = pd.read_csv("user.csv")
    index = datauser.index[datauser['chat_id'] == message.chat.id][0]
    datauser = pd.read_csv("user.csv")
    if str(message.text.split()[1]) == "C5D69F4A2B":
        datauser.loc[index, "tokens"] = 5000
    if str(message.text.split()[1]) == "P4O6I8U7Y2":
        datauser.loc[index, "status"] = 'premium'
    if str(message.text.split()[1]) in ["X9Z7K1D3C8", "L6M2N9B1V5"]:
        datauser.loc[index, "status"] = "mvp"
    datauser.to_csv('user.csv', index=False)
    bot.send_message(message.chat.id, "Промокод успешно активирован!")
    promo = message.text.split()[1]
    logger.warning(f"Promo {promo}")
    
#==========================================================
#admins commands
@bot.message_handler(commands=['send_message'])
def send_message(message):
    if message.chat.id not in admins:
        return False
    argus = message.text.split()
    if len(argus) < 2:
        bot.send_message(message.from_user.id, 'Напиши текст после комманды')
        return False
    argus.pop(0)
    txt = " ".join(argus)
    if txt == 'Update':
        txt = f"""
Aurora V5
╔═════════════╗
╟Нововведения:  
╟➣Новая система нейросетей
╟➣Добавлены токены(используются для генерации контента в нейросетях)
╟➣В группе GoPopizdim нету ограничений
╟➣У всех участников группы GoPopizdim большее количество токенов
╟➣Убрана команда /glb
╟➣Добавлена новая команда /profile
╟➣Улучшена оптимизация
                """
    logger.warning(f'Отправленно сообщение от имени бота: {txt}')
    bot.send_message(chatid, f"""{txt}""")#chatid, txt)
    bot.send_message(message.from_user.id, "Успешно отправленно!")
    
@bot.message_handler(commands=['history_clr'])
def send_message(message):
    if message.chat.id not in admins:
        return False
    argus = message.text.split()
    common_lines = []
    with open("history.txt", 'r') as file:
        for line in file:
            common_lines.append(str(line.strip() + '\n'))
    bot.send_message(message.from_user.id, str(len(common_lines)))
    file.close()
    txt = " ".join(common_lines[int(len(common_lines) - 1001):int(len(common_lines))])
    with open("history.txt", 'w') as file:
        file.write(txt)
    file.close()
    bot.send_message(message.from_user.id, "Успешно оцищенно!")
    logger.warning(f'@{message.from_user.username} Очистил историю!')
#----------------------------------------------------------      
@bot.message_handler(commands=["send_image"]) 
def send_image(message):
    if message.chat.id not in admins:
        return False
    with open("image.png", 'rb') as im:
            bot.send_photo(chatid, im)
            im.close()
    logger.warning(f'@{message.from_user.username} Отправил изображение!')
#----------------------------------------------------------   
@bot.message_handler(commands=['stats', 'info'])
def get_stats(message):
    if message.chat.id not in admins:
        return False
    current_time = datetime.datetime.now()
    current_time = current_time.replace(microsecond=0)
    time_work = current_time - start_time
    bot.send_message(message.from_user.id,f"""```Json
╔═════════════╗
╟➣Status: OK          
╟➣Time Work: "{time_work}"
╟➣Version: "{version}"
╟➣GPT_ask: "{request_gpt_coll}"
╟➣Image_gen: "{request_gen_coll}"
```""", parse_mode='MarkdownV2')
    logger.warning(f'@{message.from_user.username} Узнал инфу!')
#----------------------------------------------------------
@bot.message_handler(commands=['logs'])
def get_logs(message):
    if message.chat.id not in admins:
        return False
    bot.send_document(message.chat.id, document=open('logs.log', 'rb'))
    logger.warning(f'@{message.from_user.username} Получил логи!')
#----------------------------------------------------------
@bot.message_handler(commands=['logsclear'])
def clear_logs(message):
    if message.chat.id not in admins:
        return False
    with open('logs.log', 'w+') as log:
        log.write("\n")
    logger.warning(f'@{message.from_user.username} Очистил логи!')
    bot.send_message(message.from_user.id, "Логи очищенны!")
#----------------------------------------------------------         
#Тестовая функция для разработки
#Для отключения закомментировать!
    
@bot.message_handler(commands=['test'])
def text(message):
    pass
    # bot.send_message(message.chat.id, str(message.date - int(datetime.datetime(1970, 1, 1)).total_seconds()))
    # if message.reply_to_message != None:
    #     bot.send_message(message.chat.id, f"Reply: Сообщение: {message.reply_to_message.text}")
        
    
@bot.message_handler(commands=['opros'])
def text(message):
    if message.chat.id not in admins:
        return False
    bot.send_poll(chatid, "Как вам новая функция?", ["Сойдет", "Дно"])
    
@bot.message_handler(commands=['tex'])
def text(message):
    global tex_stat
    if message.chat.id not in admins:
        return False
    argus = message.text.split()
    argus.pop(0)
    com = str(argus[0])
    if com == 'On':
        bot.send_message(chatid, '🕐Бот закрыт на тех. работы!🕐')
        logger.warning(f'@{message.from_user.username} Включил тех работы!')
        tex_stat = True
    if com == 'Off':
        bot.send_message(chatid, '✅Бот восcтановлен и работает в нормальном режиме!✅')
        logger.warning(f'@{message.from_user.username} Выключил тех работы!')
        tex_stat = False
#---------------------------------------------------------
@bot.message_handler(commands=['Easter'])
def Easter(message):
    import random
    logger.warning(f'@{message.from_user.username} Нашел посхалку!!!!!!!!')
    rand_num = 1#random.randint(0,5)
    if rand_num == 1:
        bot.send_message(message.from_user.id, ".       ⣄⡀⠀⠀⠀⠀⠀⠀⣠⡇\n⠀⠀⠀⣻⣿⣶⣤⣀⢈⣀⣲⣷⣿⡄⠀⠀⠀\n⠀⠀⠀⣾⣿⣿⣿⣷⣿⣿⣿⣿⣷⣿⡆⠀⠀⠀⠀⠀⠀\n⠀⠀⢠⣾⣛⢿⠿⢿⣿⣿⣿⣛⣹⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⣸⣿⣿⣿⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠜⣿⡟⠸⣿⣿⣿⢙⣿⣿⣿⣿⣿⣿⣿⣿⠑⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⣿⣗⠰⠘⡹⡏⣀⡟⣿⣿⣿⣿⣿⣿⣿⢆⠀⠀⠀⠀⡀⢀⣀⠀⠀⠀⠀⠀\n⠀⠘⣿⣽⠀⠀⠁⠁⠘⠽⢻⣿⡏⣹⣿⡿⣿⠁⠉⢀⣤⣾⣾⣿⣿⠗⠋⠁⠀⠀\n⠀⠀⠸⡸⣦⠀⠀⠀⠀⠀⣸⣿⣧⣿⣿⡗⠃⠀⣐⣾⣿⣿⣿⠛⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠙⣷⣶⣲⣷⣄⡾⣽⣟⣛⣛⣛⡓⠶⣟⣿⣿⡿⣵⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⣿⣿⣿⣿⣫⣿⣽⣿⣶⣶⣶⣿⡞⠘⣿⣿⣿⣷⣦⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⢹⢿⢏⣻⣿⣿⣿⣿⣿⣿⣿⡗⠀⠀⠈⠻⣿⣿⣿⣧⢨⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⢂⣼⡾⡿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠈⠻⣿⣿⣾⣆⠀⠀⠀\n⠀⠀⠀⢀⠀⠍⣿⣻⣦⣿⣿⣿⣿⣿⣿⣿⣿⣇⢂⠀⠀⠀⠀⠙⣿⣿⣿⣇⡄⠀\n⠀⠀⠀⠀⠀⢠⣧⣸⣿⣿⡿⡿⠿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⠀\n⠀⠀⠀⠀⠀⣸⣿⣿⣿⣟⣿⣾⣷⡻⣍⢽⣿⣿⡄⢀⡀⢀⡀⠀⠀⣿⣿⣿⣿⠀\n⠀⠀⠀⠀⠀⣿⣿⣿⡟⢋⣻⠿⣿⣿⣿⣷⣿⣿⣷⡄⠖⢀⠀⠈⠀⠻⣿⡟⠃⠀\n⠀⠀⠀⠀⢸⣿⣿⣿⢁⣾⣿⣿⡾⡜⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⢠⡄⠀⠀\n⠀⠀⠀⢀⣿⣿⣿⣿⢸⣿⣿⣿⣿⣵⡿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣀⣼⡗⠀⠀\n⠀⠀⠀⣸⢿⣿⣿⣿⢸⣿⣿⣿⣿⣿⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠆⠀\n⠀⠀⠠⠻⠿⣿⣭⣽⣿⣿⣿⣿⣿⣿⣷⣦⣽⣿⣿⣿⣿⣿⣿⣿⣿⡟⠉⠁⠀⠀\n⠀⠀⠘⣤⣀⣃⣀⢸⣿⣿⣿⣿⣿⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣋⣠⣴⠇⠀⠀\n⠀⠀⠀⠸⠉⠹⠇⠀⠈⣻⣿⣿⣿⠀⠀⠀⠀⠀⠫⢿⣿⣿⣿⣿⣿⠿⠏⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠠⠀⣧⣿⣿⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⡶⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢯⣿⣋⡒⢤⣄⣀⣠⡄\n")
    if rand_num == 2:
        pass
    if rand_num == 3:
        pass
    if rand_num == 4:
        pass
    if rand_num == 5:
        pass
#=========================================================
#Отправка погоды 
def send_weather():
    try:
        #Получение погоды с сайта OpenWeather
        try:
            weather_data = requests.get(url).json()
            temperature = str(round(weather_data['main']['temp']))
            humidity = str(weather_data['main']['humidity'])
            weathers = str(weather_data['weather'][0]['description'])
            weather_main = str(weather_data['weather'][0]['main'])
            wind = str(weather_data['wind']['speed'])
            bar = str(round(weather_data['main']['pressure'] * 0.750062, 1))
            vid = str(weather_data['visibility'] / 1000)
        except Exception as e:
            return False
        #Поменяйте текст под свой!
        text = (f"Доброе утро, Петербуржцы! \nВ городе сейчас: \nПогода: {weathers.title()} \nТемпература: {temperature} °C \nВлажность: {humidity}% \nВетер: {wind}m/s \nДавление: {bar}мм.рт.ст \nВидимость: {vid}km")
        if weather_main == 'Snow':
            snow_coll = weather_data['snow']['1h']
            print(snow_coll)
            text = (f"Доброе утро, Петербуржцы! \nВ городе сейчас: \nПогода: {weathers.title()} \nТемпература: {temperature} °C \nВлажность: {humidity}% \nВетер: {wind}m/s \nДавление: {bar}мм.рт.ст \nВидимость: {vid}km \nСкорость снега: {snow_coll}mm/1h")
        #Отправка в группу
        bot.send_message(chatid,text)
        logger.info(f'Погода в 8:00 успешно отправленна')
        if int(temperature) < -15:
            bot.send_message(chatid,"Чатик, не морозьте жёпки, одевайтесь теплее.")
    except Exception as e:
        logger.error(f'Ошибка в погоде. Код: {e}')
#==========================================================
#Указание функций комманд
def treager():
    while True:
        schedule.run_pending()
        sleep(1)
#----------------------------------------------------------  
def check(NowDay=0,NowMonth=0):
    try:
        # NowDate = datetime.datetime.now()
        # NowDay = NowDate.day
        # NowMonth = NowDate.month
        
        if int(data[(data['dday'] == NowDay) & (data["dmon"] == NowMonth)].shape[0]) <= 0:
            logger.info("Именников нету!")
            return False
        
        NowDR = []
        if int(data[(data['dday'] == NowDay) & (data["dmon"] == NowMonth)].shape[0]) >= 1:
            NowDR = data.index[(data['dday'] == NowDay) & (data["dmon"] == NowMonth)].tolist()
            print(NowDR)
            
        ind = 0
        for b in range(int(len(NowDR))):
            #Заменить текст на свой!
            text = "Доброго дня! Сегодня день рождения у " + data.loc[NowDR[ind],"nickname"] + ", пожелаем " + data.loc[NowDR[ind],"Username"] + " удачи, счастья, отличного настроения и всего наилучшего!\n"
            bot.send_message(chatid,"–=–=–=–=–=–=–=–=–=–=–=–\n" + text + "–=–=–=–=–=–=–=–=–=–=–=–")
            logger.info(f'Отправленно поздравление пользователю ' + data.loc[NowDR[ind],"nickname"])
            ind += 1
    except Exception as e:
        logger.error(f"Ошибка в поздравление пользователя")
#----------------------------------------------------------      
def save_new(message):
    if message.text == "Отмена" or message.text == 'отмена':
        bot.send_message(message.from_user.id, "Отменяю")
        return False
    try:
        argus = message.text.split()
        morph = pymorphy2.MorphAnalyzer()
        word_c = morph.parse(argus[0])[0]
        gent = word_c.inflect({'datv'})
        save_text = str((gent.word).title() + "," + "@" +message.from_user.username + "," + argus[1] + "," + argus[2])
        day_range = 0
        month_range = 0
        
        for i in argus[1]:
            day_range += 1
            if i == "0":
                #Заменить текст на свой!
                bot.send_message(message.from_user.id, "Я же сказал без нулей. Попробуй снова.")
                bot.send_message(message.from_user.id, "Отправь данные без нулей через пробелы в формате: Name Nickname Day Month. Пример: Виктор @Test 1 5")
                bot.register_next_step_handler(message,save_new)
                return False
        
        for i in argus[2]:
            month_range += 1
            if i == "0":
                #Заменить текст на свой!
                bot.send_message(message.from_user.id, "Я же сказал без нулей. Попробуй снова.")
                bot.send_message(message.from_user.id, "Отправь данные без нулей через пробелы в формате: Name Nickname Day Month. Пример: Виктор @Test 1 5")
                bot.register_next_step_handler(message,save_new)
                return False
        if day_range > 2 or day_range < 1 or month_range > 2 or day_range < 1 or int(argus[1]) > 31 or int(argus[2]) > 12:
            #Заменить текст на свой!
            bot.send_message(message.from_user.id, "Такой даты не существует. Попробуй снова.")
            bot.send_message(message.from_user.id, "Отправь данные без нулей через пробелы в формате: Name Nickname Day Month. Пример: Виктор @Test 1 5")
            bot.register_next_step_handler(message,save_new)
            return False
        
        with open('NewData.txt', 'a') as f:
            f.write(save_text + '\n')
        #Заменить текст на свой!
        bot.send_message(message.from_user.id, "Ладно-ладно, записал, отстань")
        logger.info(f'Записан новый пользователь в базу данных: {save_text}')
        f.close()
    except Exception as e:
        # Заменить текст на свой!
        bot.send_message(message.from_user.id, "У вас что-то не правильно. Попробуйте снова.")
        bot.send_message(message.from_user.id, "Отправь данные без нулей через пробелы в формате: Name Nickname Day Month. Пример: Виктор @Test 1 5")
        bot.register_next_step_handler(message,save_new)
        logger.error(f"Ошибка в добавление нового пользователя! Код: {e}")
        return False

def add_tokens_all():
    datauser = pd.read_csv("user.csv")
    for i in range(datauser.shape[0]):
        if str(datauser.loc[i, 'status']) == 'default':
            datauser.loc[i, 'tokens'] = 250
        if str(datauser.loc[i, 'status']) == 'group':
            datauser.loc[i, 'tokens'] = 800
        if str(datauser.loc[i, 'status']) == 'vip':
            datauser.loc[i, 'tokens'] = 1000
        if str(datauser.loc[i, 'status']) == 'premium':
            datauser.loc[i, 'tokens'] = 250
    datauser.to_csv('user.csv', index=False)
#==========================================================
#Запись истории чата
@bot.message_handler(func=lambda message: message.chat.id == int(chatid), content_types=['text'])
def write_chat_history(message):
    if True:
        message_text = str(message.text)
        message_username = str(message.from_user.username)
        save_text = str(message_username + ":" + message_text + '\n')
        with open("history.txt", 'a', encoding='utf-8') as file:
            file.write(str(save_text))
        file.close()

@bot.message_handler(func=lambda message: message.chat.id != int(chatid), content_types=['text'])
def localchatgpt(message):
    if message.chat.type == 'private':
        ask_chatgpt(message, chat_state=False)

def log(text):
    for i in range(len(push_message_admin)):
        bot.send_message(push_message_admin[i], text)
#==========================================================
#Установка таймеров
schedule.every().sunday.at("00:00").do(add_tokens_all)
schedule.every().day.at(Weather_time).do(send_weather)
schedule.every().day.at(Gift_time).do(check)   

#Установка и запуск потоков
threading_treager = threading.Thread(target=treager)
threading_treager.start()

# Ручное поздравленние
# Раскоментировать стоку ниже, указать сегодняшний день и месяц и перезапутить скрипт
# check(NowDay=10, NowMonth=2)

#==========================================================
#Запуск бота
logger.info("Бот запущен!")
log("Бот старт!")
# check(5,5)
try:
# if True:
    bot.infinity_polling()
except Exception as e:
    logger.error(f"[Error] Time out. code: {e}")
    # import Config_bot
    # Config_bot.reloader()
