#===================================================#
# ░█████╗░██╗░░░██╗██████╗░░█████╗░██████╗░░█████╗░ #
# ██╔══██╗██║░░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗ #
# ███████║██║░░░██║██████╔╝██║░░██║██████╔╝███████║ #
# ██╔══██║██║░░░██║██╔══██╗██║░░██║██╔══██╗██╔══██║ #
# ██║░░██║╚██████╔╝██║░░██║╚█████╔╝██║░░██║██║░░██║ #
# ╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝ #
#===================================================#

# from os import error
from datetime import datetime
import schedule
import threading
from time import sleep
from logzero import logger, logfile, loglevel, logging
from sys import exit

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import telebot

# from Aurora_bot import NowDR
import Dependencies.BackGround as BackGround
import Dependencies.DataBase as DataBase

#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
# Bot_config
bot_token = "6904577368:AAHMjsneMF0HaLHiWa08Bv2ZzBZOwIJ7yTo" #Aurora
# bot_token = "6601620934:AAGvgH9rDE4JHrUBThkrXrca9zfJIpMeh0Q" #BotTest
        # main        # second
admins = [1746901164, 1018366370]#, 1467854871]
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
# Logs
logfile("logs/logs.log")
logfile("logs/deplogs.log", loglevel=logging.DEBUG)
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
usage_ask = 1
usage_gen = 0
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
# AI config
base_model = "gpt-3.5-turbo-16k-0613"
# base_model = "gpt-4o"
    # ChatGPT
open_ai_token = "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"
    # GigaChat
gigachat_token = "Y2Q4ZmU4YWEtOWE5OS00OGU4LWExNjEtM2U2YWE2Y2NlYzYwOjQzNzI4YjE4LWM1YzAtNDIzYy1iZTA0LWE2OTE1YjE5Yzc3Zg=="
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
# Weather config
base_city = "Saint%20Petersburg"
weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={base_city}&units=metric&lang=ru&appid=c38e5a3db7bd33d13d9d0c37f83ccdec'
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
#Donate config
donate_url = 'https://boosty.to/vitusik_kentusik.org/donate'
ask_coll = 5
gen_coll = 5
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
#Bot config
version = 'v6'
technical_brake = False
gp_id = '-1001665880322'
fresh_time = 5 #In minutes
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
#time 
start_time = datetime.now().replace(microsecond=0)
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
# Config
bot = telebot.TeleBot(bot_token)
# data = pd.read_csv("DateFrame.csv")
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
Censored_path = "Add-ons/censored.png"
#FrontEnd
#! Поменять на актуальные комманды
@bot.message_handler(commands=["help"])
def help(message):
    ms_text = f"""
/add - Добавиться в базу данных 
/ask Вопрос - Задать вопрос chatGPT
/gen ПРОМТ - сгенерировать изображение
/profile - вывести данные об аккаунте
/weather - Вывести погоду в Питере
/weather ГОРОД - Вывести погоду в городе 
/forecast - Вывести прогноз погоды 
VGF©                    Aurora{version}"""
    bot.send_message(message.chat.id, ms_text)
    
    logger.info(f"{message.from_user.username} вывел help!")
    

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Привет! Я - нейросетевой бот AuroraBot {version}, и я здесь, чтобы повеселиться. Я могу помочь тебе в разных задачах /help. Я люблю общаться с людьми и узнавать что-то новое. Давай пообщаемся!")
    logger.info(f"@{message.from_user.username} вывел start!")

#add
@bot.message_handler(commands=["profile"])
def profile(message, isBack=False):
    try:
        logger.info(f"@{message.from_user.username} Начал запрос к профилю")
        
        if BackGround.chenkChatType(message): 
            bot.send_message(message.chat.id, "❌Напиши команду боту в личные сообщения")
            
            logger.info(f"@{message.from_user.username} ❌Напиши команду боту в личные сообщения")
            return False

        if (technical_brake) & (message.chat.id not in admins): 
            bot.send_message(message.chat.id, "❌Идут тех. работы! Попробуйте позже!")
            
            logger.info(f"@{message.from_user.username} ❌Идут тех. работы! Попробуйте позже!")
            return False

        # profile_data = DataBase.get_profile(message, bot.get_chat_member(gp_id, message.from_user.id).status)
        
        profile_data = DataBase.get_profile(message, bot.get_chat_member(gp_id, message.from_user.id).status)
        
        logger.info(f"@{message.from_user.username} {profile_data}")

        if not isBack:
            DataBase.check.CurentNickname(message)
            logger.info(f"@{message.from_user.username} Проверка на коректность никнейма")

        ms_text = f"""
        ⭐️Профиль
        📕Имя: {profile_data[0]}
        ⚙️Модель: {profile_data[3]}
        📖Статус: {profile_data[1]}
        💲Токены: {profile_data[2]}
        📸Фотографий: {profile_data[4]}
        """

        markup = types.InlineKeyboardMarkup()
        change_btn = types.InlineKeyboardButton("⚙️Изменить модель", callback_data="change_model")
        status_btn = types.InlineKeyboardButton("📖Купить статус", callback_data="buy_status")
        tokens_btn = types.InlineKeyboardButton("💲Купить токены", callback_data="buy_tokens")
        images_btn = types.InlineKeyboardButton("📸Купить фотографии", callback_data="buy_images")

        markup.add(change_btn, status_btn, tokens_btn, images_btn)

        if isBack:
            bot.edit_message_text(ms_text, message.chat.id, message.message_id, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, ms_text, reply_markup=markup)

        logger.info(f"@{message.from_user.username} Вывел профиль")
        
    except Exception as error:
        logger.error(f"Ошибка профиля! \n Код: {error}")
        return False


@bot.message_handler(commands=["add"])
def add(message):
    ch_id = message.chat.id
    
    logger.info(f"@{message.from_user.username} ❌Идут тех. работы! Попробуйте позже!")
    if str(message.chat.type) != 'private': bot.send_message(message.chat.id, "❌Напиши команду боту в личные сообщения"); return False
    
    if (technical_brake) & (message.chat.id not in admins): 
        bot.send_message(message.chat.id, "❌Идут тех. работы! Попробуйте позже!")
        return False
    
    if bot.get_chat_member(gp_id, message.from_user.id).status == 'left': 
        bot.send_message(message.chat.id, text="❌Вы не являетесь участником группы.")
        return False
    
    if message.text.split()[0] != '/add':
        if BackGround.add.checkCanceled(message.text): bot.send_message(ch_id, "Отменил!"); return False
    
        addResualt = BackGround.add.addNewUser(message)

        if addResualt == True:
            bot.send_message(ch_id, "✅Ладно-ладно, записал, отстань")
            logger.warning(f'Записан новый пользователь в базу данных!')

            return True

        elif addResualt == False:
            bot.send_message(ch_id, "❌У вас что-то не правильно. Попробуйте снова.")

            logger.error(f"Ошибка в добавление нового пользователя!")

            bot.send_message(ch_id, "Отправь данные без нулей через пробелы в формате: Name Nickname Day Month. Пример: Виктор @Test 1 5")
            bot.register_next_step_handler(message, add)
        else:
            bot.send_message(ch_id, addResualt)
            bot.send_message(ch_id, "Отправь данные без нулей через пробелы в формате: Name Nickname Day Month. Пример: Виктор @Test 1 5")
            bot.register_next_step_handler(message, add)
    else:
        bot.send_message(ch_id, "Отправь данные без нулей через пробелы в формате: Name Nickname Day Month. Пример: Виктор @Test 1 5")
        
        bot.register_next_step_handler(message, add)
        

@bot.message_handler(commands=["forecast"])
def forecast(message):
    loading_message = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше сообщение обрабатывается")
    loading_message
    try:
        command_split = message.text.split()

        if (technical_brake) & (message.chat.id not in admins): 
            bot.edit_message_text("❌Идут тех. работы! Попробуйте позже!", message.chat.id, loading_message.message_id)
            return False

        if len(command_split) > 1:
            command_split.pop(0)
            sity = " ".join(command_split)
        else:
            sity = "Санкт-петербург"

        # try:
        if True:
            weather_text = BackGround.weather.GetForecast(sity)
        # except:
            # send_error(loading_message, "❌В названии города ошибка. Попробуйте снова!")
            
            # return False

        weather_text = BackGround.markdown_convert(weather_text)
        
        bot.edit_message_text(weather_text, message.chat.id, loading_message.message_id, parse_mode="MarkdownV2")

        logger.info(f"@{message.from_user.username} вывел прогноз погоды")
        
    except Exception as error:
        bot.edit_message_text("❌Возникла ошибка. Наша команда уже работает над ее исправлением!", message.chat.id, loading_message.message_id)
        
        logger.error(f"Ошибка в погоде: {error}") 
        
        return False
        
        
@bot.message_handler(commands=["dailyforecast"])
def forecastperday(message):
    try:
        command_split = message.text.split()

        loading_message = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше сообщение обрабатывается")
        loading_message

        if (technical_brake) & (message.chat.id not in admins): 
            bot.edit_message_text("❌Идут тех. работы! Попробуйте позже!", message.chat.id, loading_message.message_id)
            return False

        if len(command_split) > 1:
            command_split.pop(0)
            sity = " ".join(command_split)
        else:
            sity = "Санкт-петербург"

        try:
            weather_text = BackGround.weather.GetForecastPerDay(sity)
        except:
            send_error(loading_message, "❌В названии города ошибка. Попробуйте снова!")
            
            return False

        weather_text = BackGround.markdown_convert(weather_text)
        
        bot.edit_message_text(weather_text, message.chat.id, loading_message.message_id, parse_mode="MarkdownV2" )

        logger.info(f"@{message.from_user.username} вывел прогноз погоды")
        
    except Exception as error:
        logger.error(f"Ошибка в погоде: {error}") 
        send_error(loading_message, "❌В названии города ошибка. Попробуйте снова!")
        

@bot.message_handler(commands=["weather"])
def weather(message):
    loading_message = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше сообщение обрабатывается")
    loading_message
    try:
        command_split = message.text.split()


        if (technical_brake) & (message.chat.id not in admins): 
            bot.edit_message_text("❌Идут тех. работы! Попробуйте позже!", message.chat.id, loading_message.message_id)
            return False

        if len(command_split) > 1:
            command_split.pop(0)
            sity = " ".join(command_split)
        else:
            sity = "Санкт-петербург"

        try:
            weather_text = BackGround.weather.GetWeather(sity)
        except:
            send_error(loading_message, "❌В названии города ошибка. Попробуйте снова!")
            
            return False

        bot.edit_message_text(weather_text, message.chat.id, loading_message.message_id)

        logger.info(f"@{message.from_user.username} вывел погоду")
        
    except Exception as error:
        bot.edit_message_text("❌Возникла ошибка. Наша команда уже работает над ее исправлением!", message.chat.id, loading_message.message_id)
        
        logger.error(f"Ошибка в погоде: {error}") 


@bot.message_handler(commands=["tempmetrics"])
def metrics(message):
    command_split = message.text.split()

    loading_message = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше сообщение обрабатывается")
    loading_message
    
    if (technical_brake) & (message.chat.id not in admins): 
        bot.edit_message_text("❌Идут тех. работы! Попробуйте позже!", message.chat.id, loading_message.message_id)
        return False
    
    if len(command_split) > 1:
        command_split.pop(0)
        sity = " ".join(command_split)
    else:
        sity = "Санкт-петербург"
        
    try:
        photo_metrics = BackGround.weather.create_temp_metric(sity)
    except:
        send_error(loading_message, "❌В названии города ошибка. Попробуйте снова!")
        
        return False
    
    logger.info(f"@{message.from_user.username} вывел метрику температуры")
    
    bot.send_photo(message.chat.id, photo=photo_metrics)
    
    bot.delete_message(message.chat.id, loading_message.message_id)
    

@bot.message_handler(commands=["sum"])
def sum(message):
    loading_mess = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше сообщение обрабатывается")
    loading_mess
    try:
        
        logger.info(f"@{message.from_user.username} Начал запрос sum")
        
        ch_id = message.chat.id
        
        # Проверка на техничесские работы
        if (technical_brake) & (message.chat.id not in admins): 
            bot.edit_message_text("❌Идут тех. работы! Попробуйте позже!", ch_id, loading_mess.message_id)
            return False
        
        if str(message.chat.id) != str(gp_id):
            send_error(loading_mess, "❌Напиши команду в группе")
            return False
        
        # Проверка на участника группы
        if bot.get_chat_member(gp_id, message.from_user.id).status == 'left': 
            send_error(loading_mess, "❌Вы не являетесь участником группы.")
            return False
        # Проверка на свежость запроса
        
        if BackGround.freshcheck(message, fresh_time): 
            send_error(bot_ms=loading_mess, error_text="❌Запрос устарел. Попробуйте снова!")
            return False
            
        if BackGround.summoryzen.CheckSumNumberInRange(summorysen_coll):
            send_error(loading_mess.message_id, text="❌Значения для суммирования: 50,100,150,350. Попробуйте снова.")
            return False
        
        summorysen_coll = BackGround.summoryzen.GetSummorysenNumber(message)
        
        
        get_text = BackGround.summoryzen.GetLines(summorysen_coll)
        
        promt = f'Суммируй эти сообщения обязательно с упоминанием пользователей и что они писали кратко и обрабатывая каждое сообщение не списком а целым текстом без общей темы в конце и с капелькой дичи объем: 0.5 страниц: {get_text}'
        if summorysen_coll <= 100:
            promt = f'Суммируй эти сообщения обязательно с упоминанием пользователей и что они писали обрабатывая каждое сообщение не списком а целым текстом без общей темы в концеи с капелькой дичи  объем: 1 страниц: {get_text}'
        if summorysen_coll >= 150:
            promt = f'Суммируй эти сообщения обязательно с упоминанием пользователей и что они писали обрабатывая каждое сообщение не списком а целым текстом без общей темы в конце и с капелькой дичи  очееень длинно и развернуто в 10 страниц: {get_text}'
            
        summorysen_text = BackGround.ask.askGPT(promt, "gpt-3.5-turbo-0125", token=open_ai_token)
        summorysen_text = str(f"Aurora-{version} - Последние {summorysen_coll} cообщений суммированны так: \n{summorysen_text}")
        
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("❤️Поддержать автора", url=donate_url)
        markup.add(btn)
        
        bot.edit_message_text(chat_id=message.chat.id, message_id=loading_mess.message_id, text=str(summorysen_text))
        
        logger.info(f'@{message.from_user.username} суммировал {summorysen_coll} сообщений')
        
    except Exception as error:
        bot.edit_message_text("❌Возникла ошибка. Наша команда уже работает над ее исправлением!", ch_id, loading_mess.message_id)
        
        logger.error(f"Ошибка sum \nКод: {error}")
        
        return False


@bot.message_handler(commands=["ask", "gpt"])
def ask(message, chat_is_local = True):
    global usage_ask
    # if True:
    loading_mess = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше сообщение обрабатывается")
    loading_mess
    try:
        
        logger.info(f"@{message.from_user.username} Начал запрос gpt")
        
        ch_id = message.chat.id
        
        # Проверка на техничесские работы
        if (technical_brake) & (message.chat.id not in admins): 
            bot.edit_message_text("❌Идут тех. работы! Попробуйте позже!", ch_id, loading_mess.message_id)
            return False
        # Проверка на свежость запроса
        if BackGround.freshcheck(message, fresh_time): 
            send_error(bot_ms=loading_mess, error_text="❌Запрос устарел. Попробуйте снова!")
            return False
        # Проверка на то что у пользователя есть никнейм
        if message.from_user.username == None: 
            send_error(bot_ms=loading_mess, error_text="❌Прежде чем использовать комманду /ask, надо установить никнейм!")
            return False
        
        user_promt = message.text
        
        #Проверка на локальный чат
        if chat_is_local:
            # Проверка на правильность промта
            if BackGround.checkPromt(user_promt):
                user_promt = BackGround.getPromt(user_promt)
            else:
                send_error(bot_ms=loading_mess, error_text="❌Нужно ввести промт после команды. Попробуйте снова!")
                return False
        
        if DataBase.check.NotAvailabilityUser(message):
            DataBase.check.add_user(message, bot.get_chat_member(gp_id, message.from_user.id).status)
        # DataBase.check.NotAvailabilityUser(message, gp_id=gp_id, user_status=bot.get_chat_member(gp_id, message.from_user.id).status)
        
        user_gpt_model = DataBase.getCurrentModel(message)
        if user_gpt_model in ["gpt-4-turbo", 'gpt-4-turbo-24-04-09', "gpt-4-1106-preview"]:
            usage_tokens = BackGround.mathToken(text=user_promt, is_gpt4=True)
        else:
            usage_tokens = BackGround.mathToken(text=user_promt)
            
        # Проверка наличия ответа на сообщение
        if message.reply_to_message != None: user_promt = f"{user_promt}: {message.reply_to_message.text}"
        
        if DataBase.check.tokens_ask(message, usage_tokens):
            markup = types.InlineKeyboardMarkup()
            tokens_btn = types.InlineKeyboardButton("💲Купить токены", callback_data="buy_tokens")
            markup.add(tokens_btn)
            
            bot.edit_message_text("❌Недостаточно токенов!", message.chat.id, loading_mess.message_id, markup=markup)
            return False
        
        if message.chat.id != gp_id:
            DataBase.check.add_user(message, bot.get_chat_member(gp_id, message.from_user.id).status)
        
        DataBase.subtraction_tokens.ask(message, usage_tokens)
        
        answer_text = BackGround.ask.askGPT(user_promt, user_gpt_model, open_ai_token)
        
        ms_text = f"{BackGround.markdown_convert(answer_text)}"
        
        if DataBase.check.ShowLastToken(message.chat.id, gp_id): 
            ms_text = f"{ms_text} \n{BackGround.Tokens.GetLastTokens(message, usage_tokens, DataBase.get_last_tokens(message))}"
        
        
        if (usage_ask % ask_coll) == 0:
            markup = types.InlineKeyboardMarkup()
            btn_adv = types.InlineKeyboardButton("❤️Поддержать автора", url=donate_url)
            markup.add(btn_adv)
            bot.edit_message_text(f"""{ms_text}""", ch_id, loading_mess.message_id, reply_markup=markup, parse_mode='MarkdownV2')
        else:
            bot.edit_message_text(f"""{ms_text}""", ch_id, loading_mess.message_id, parse_mode='MarkdownV2')
            
        usage_ask += 1
        
        logger.info(f"@{message.from_user.username} Использовал GPT \nPromt: {user_promt} \nAverage: {answer_text} \nTokens: {usage_tokens}")
    except Exception as error:
        bot.edit_message_text("❌Возникла ошибка. Наша команда уже работает над ее исправлением!", ch_id, loading_mess.message_id)
    
        logger.error(f"Ошибка GPT \nКод: {error}")
        
        return False
        

@bot.message_handler(commands=["gen", "generate", "image"])
def generate(message):
    global usage_gen
    loading_mess = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше сообщение обрабатывается")
    loading_mess
    
    try:
        
        logger.info(f"@{message.from_user.username} Начал запрос gen")
        
        ch_id = message.chat.id
        
        # Проверка на техничесские работы
        if (technical_brake) & (message.chat.id not in admins): 
            bot.edit_message_text("❌Идут тех. работы! Попробуйте позже!", ch_id, loading_mess.message_id)
            return False
        # Проверка на свежость запроса
        if BackGround.freshcheck(message, fresh_time): 
            send_error(bot_ms=loading_mess, error_text="❌Запрос устарел. Попробуйте снова!")
            return False
        
        # Проверка на то что у пользователя есть никнейм
        if message.from_user.username == None: 
            send_error(bot_ms=loading_mess, error_text="❌Прежде чем использовать комманду /ask, надо установить никнейм!")
            return False
        
        user_promt = message.text
        
        # Проверка на правильность промта
        if BackGround.checkPromt(user_promt): user_promt = BackGround.getPromt(user_promt)
        else:
            send_error(bot_ms=loading_mess, error_text="❌Нужно ввести промт после команды. Попробуйте снова!")
            return False

        if DataBase.check.images_gen(message):
            markup = types.InlineKeyboardMarkup()
            images_btn = types.InlineKeyboardButton("📸Купить фотографии", callback_data="buy_images")
            markup.add(images_btn)
            
            bot.edit_message_text("❌Недостаточно картин!", message.chat.id, loading_mess.message_id, markup=markup)
            return False
        
        GenImagesData = BackGround.gen.ImageGenerator(promt=user_promt)
        model_id = BackGround.gen.GetKandiskyModel()
        
        if BackGround.gen.CheckLenImages(images=GenImagesData):
            send_error(bot_ms=loading_mess, error_text="❌Долгий ответ сервера. Попробуйте снова!")
            return False
        
        if BackGround.gen.CheckCensored(images=GenImagesData):
            with open(Censored_path, 'rb') as image:
                bot.send_photo(ch_id, image, caption="❌Промт зацензурен. Генерация невозможна")
                bot.delete_message(ch_id, loading_mess.message_id)
                
                return False
        
        if DataBase.check.subscribe(message, bot.get_chat_member(-1002064516590, message.from_user.id).status):
            send_error(loading_mess, "❌Для начала работы с нейросетями подпишитесь на канал @Aurorafloodbot_info и повторите попытку")
            
            return False
        
        if DataBase.check.NotAvailabilityUser(message):
            DataBase.check.add_user(message, bot.get_chat_member(gp_id, message.from_user.id).status)
        
        DataBase.subtraction_tokens.gen(message)
        
        generatedImage = BackGround.gen.ConvertImage(GenImagesData['images'][0])
        
        if usage_gen % gen_coll == 0:
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("❤️Поддержать автора", url=donate_url)
            markup.add(btn)
            
            if DataBase.check.ShowLastToken(message.chat.id, gp_id):
                bot.send_photo(message.chat.id, generatedImage, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово {BackGround.Tokens.GetLastImages(message, DataBase.get_last_images(message))}"), reply_markup=markup)
            else:
                bot.send_photo(message.chat.id, generatedImage, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово"), reply_markup=markup)
        else:
            if DataBase.check.ShowLastToken(message.chat.id, gp_id):
                bot.send_photo(message.chat.id, generatedImage, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово {BackGround.Tokens.GetLastImages(message, DataBase.get_last_images(message))}"))
            else:
                bot.send_photo(message.chat.id, generatedImage, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово"), reply_markup=markup)
                
        bot.delete_message(message.chat.id, message_id=loading_mess.message_id)
        
        usage_gen += 1
        
        logger.info(f"@{message.from_user.username} Использовал GEN \nPromt: {user_promt}")
        
    except Exception as error:
        bot.edit_message_text("❌Возникла ошибка. Наша команда уже работает над ее исправлением!", ch_id, loading_mess.message_id)
        
        logger.error(f"Ошибка GEN \nКод: {error}")
        
        return False


@bot.message_handler(commands=['easter'])
def Easter(message):
    logger.warning(f'@{message.from_user.username} Нашел посхалку!!!!!!!!')
    
    bot.send_message(message.from_user.id, ".       ⣄⡀⠀⠀⠀⠀⠀⠀⣠⡇\n⠀⠀⠀⣻⣿⣶⣤⣀⢈⣀⣲⣷⣿⡄⠀⠀⠀\n⠀⠀⠀⣾⣿⣿⣿⣷⣿⣿⣿⣿⣷⣿⡆⠀⠀⠀⠀⠀⠀\n⠀⠀⢠⣾⣛⢿⠿⢿⣿⣿⣿⣛⣹⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⣸⣿⣿⣿⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠜⣿⡟⠸⣿⣿⣿⢙⣿⣿⣿⣿⣿⣿⣿⣿⠑⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⣿⣗⠰⠘⡹⡏⣀⡟⣿⣿⣿⣿⣿⣿⣿⢆⠀⠀⠀⠀⡀⢀⣀⠀⠀⠀⠀⠀\n⠀⠘⣿⣽⠀⠀⠁⠁⠘⠽⢻⣿⡏⣹⣿⡿⣿⠁⠉⢀⣤⣾⣾⣿⣿⠗⠋⠁⠀⠀\n⠀⠀⠸⡸⣦⠀⠀⠀⠀⠀⣸⣿⣧⣿⣿⡗⠃⠀⣐⣾⣿⣿⣿⠛⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠙⣷⣶⣲⣷⣄⡾⣽⣟⣛⣛⣛⡓⠶⣟⣿⣿⡿⣵⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⣿⣿⣿⣿⣫⣿⣽⣿⣶⣶⣶⣿⡞⠘⣿⣿⣿⣷⣦⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⢹⢿⢏⣻⣿⣿⣿⣿⣿⣿⣿⡗⠀⠀⠈⠻⣿⣿⣿⣧⢨⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⢂⣼⡾⡿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠈⠻⣿⣿⣾⣆⠀⠀⠀\n⠀⠀⠀⢀⠀⠍⣿⣻⣦⣿⣿⣿⣿⣿⣿⣿⣿⣇⢂⠀⠀⠀⠀⠙⣿⣿⣿⣇⡄⠀\n⠀⠀⠀⠀⠀⢠⣧⣸⣿⣿⡿⡿⠿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⠀\n⠀⠀⠀⠀⠀⣸⣿⣿⣿⣟⣿⣾⣷⡻⣍⢽⣿⣿⡄⢀⡀⢀⡀⠀⠀⣿⣿⣿⣿⠀\n⠀⠀⠀⠀⠀⣿⣿⣿⡟⢋⣻⠿⣿⣿⣿⣷⣿⣿⣷⡄⠖⢀⠀⠈⠀⠻⣿⡟⠃⠀\n⠀⠀⠀⠀⢸⣿⣿⣿⢁⣾⣿⣿⡾⡜⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⢠⡄⠀⠀\n⠀⠀⠀⢀⣿⣿⣿⣿⢸⣿⣿⣿⣿⣵⡿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣀⣼⡗⠀⠀\n⠀⠀⠀⣸⢿⣿⣿⣿⢸⣿⣿⣿⣿⣿⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠆⠀\n⠀⠀⠠⠻⠿⣿⣭⣽⣿⣿⣿⣿⣿⣿⣷⣦⣽⣿⣿⣿⣿⣿⣿⣿⣿⡟⠉⠁⠀⠀\n⠀⠀⠘⣤⣀⣃⣀⢸⣿⣿⣿⣿⣿⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣋⣠⣴⠇⠀⠀\n⠀⠀⠀⠸⠉⠹⠇⠀⠈⣻⣿⣿⣿⠀⠀⠀⠀⠀⠫⢿⣿⣿⣿⣿⣿⠿⠏⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠠⠀⣧⣿⣿⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⡶⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢯⣿⣋⡒⢤⣄⣀⣠⡄\n")


@bot.message_handler(commands=["getId"])
def getId(message):
    bot.send_message(message.chat.id, str(message.chat.id))
    
@bot.message_handler(commands=["test"])
def test(message):
    DataBase.giveAllTokens()
    
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
@bot.message_handler(commands=["sudo"], func=lambda message: message.chat.id in admins)
def sudo(message):
    ch_id = message.chat.id
    
    command_split = message.text.split()
    if len(command_split) < 2: 
        text = """
```
/sudo info
```
Выводит статистику
```
/sudo GetChatId (1 userName)
```
Получить чат айди по ник нему (1)

```
/sudo sendMessage (1 text) (2 chat_id)
```
Выводит сообщение (1) в определенный чат (2)

```
/sudo logs (1 num)
```
Выводит (1) строчек лога

```
/sudo clearLogs
```
Очишает логи

```
/sudo setStatus (1 status) (2 user chatid)
``` 
Устанавливает (1) статус пользователю (2)

```
/sudo giveTokens (1 num) (2 user chatid)
``` 
Выдает (1) количество токенов пользователю (2)

```
/sudo giveImages (1 num) (2 user chatid)
``` 
Выдает (1)  количество фотографий пользователю (2)
```
/sudo stop
```
Отстанавливает бота 

/sudo - выводит все админ команды
                         """
        text = BackGround.markdown_convert(text)
        
        bot.send_message(ch_id, text,parse_mode="MarkdownV2")
        logger.warning(f'@{message.from_user.username} Вывел хомяк!')
        return True
    
    match str(command_split[1]):
        case "GetChatId":
            if len(command_split) < 3: 
                bot.send_message(ch_id, "❌Недостаточно аргументов")
                return False
            
            bot.send_message(ch_id, DataBase.check.user(str(command_split[2])))
            
            
        case "logs":
            if len(command_split) < 3: 
                bot.send_messge(ch_id, "❌Недостаточно аргументов")
                return False
            
            bot.send_message(ch_id, BackGround.logs.get_logs(int(command_split[2])))
            
            logger.warning(f'@{message.from_user.username} Вывел логи!')
        
        
        case "clearLogs":
            BackGround.logs.clearLogs()
            bot.send_message(ch_id, "✅Успешно очищенно")
            
            logger.warning(f'@{message.from_user.username} Очистил логи!')
        
        
        case "info":
            current_time = datetime.now().replace(microsecond=0)
            time_work = current_time - start_time
            bot.send_message(message.from_user.id,f"""```Json
╔═════════════╗
╟➣Статус: OK          
╟➣Время работы: "{time_work}"
╟➣Тех работы: "{technical_brake}"
╟➣GPT запросов: "{usage_ask}"
╟➣GEN запросов: "{usage_gen}"
╟➣Версия: "{version}"
```""", parse_mode='MarkdownV2')
            logger.warning(f'@{message.from_user.username} Узнал инфу!')
        
        
        case "sendMessage":
            if len(command_split) < 4: 
                bot.send_message(ch_id, "❌Недостаточно аргументов")
                return False
            try:
                if str(command_split[2]) == "GP":
                    bot.send_message(gp_id, str(command_split[3]))
                else:
                    bot.send_message(command_split[2], str(command_split[3]))
                    
                bot.send_message(ch_id, "✅Успешно отправленно")
            except Exception as error:
                bot.send_message(ch_id, str(error))
        
        
        case "tokens":
            if len(command_split) < 5: 
                bot.send_message(ch_id, "❌Недостаточно аргументов")
                return False
            
            print(command_split[2])
            print(command_split[3])
            command_split[4] = str(command_split[4]).replace("@", "")
            print(command_split[4])
            
            if command_split[2] not in ["give", "set"]:
                bot.send_message(ch_id, "❌Неверное действие. set или give")
                return False
            
            if str(command_split[2]) == "give":
                bot.send_message(ch_id, DataBase.giveTokens(command_split[4], command_split[3]))
            elif str(command_split[2] == 'set'):
                bot.send_message(ch_id, DataBase.setTokens(command_split[4], command_split[3]))
        
        
        case "images":
            if len(command_split) < 5: 
                bot.send_message(ch_id, "❌Недостаточно аргументов")
                return False
            
            if str(command_split[2]) not in ["give", "set"]:
                bot.send_message(ch_id, "❌Неверное действие. set или give")
                return False
            
            if str(command_split[2]) == "give":
                bot.send_message(ch_id, DataBase.giveImage(command_split[4], command_split[3]))
            elif str(command_split[2] == 'set'):
                bot.send_message(ch_id, DataBase.setImage(command_split[4], command_split[3]))
        
        
        case "setStatus":
            if len(command_split) < 4: 
                bot.send_mesфsge(ch_id, "❌Недостаточно аргументов")
                return False
            
            bot.send_message(ch_id, DataBase.setStatus(command_split[3], command_split[2]))
           
            
        case "stop":
            exit()
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
def show_models(message):
    ch_id = message.chat.id
    
    markup = types.InlineKeyboardMarkup()
    
    models = DataBase.get_models(message.chat.id)
    
    for model in models:
        btn = types.InlineKeyboardButton(f"⚙️ {model}", callback_data=f"change {model}")
        markup.add(btn)
    
    back_button = types.InlineKeyboardButton(f"Назад", callback_data=f"profile")
    markup.add(back_button)
    
    bot.edit_message_text("Выберете модель: ", ch_id, message.message_id, reply_markup=markup)


def show_status(message):
    ch_id = message.chat.id
    
    markup = types.InlineKeyboardMarkup()
    
    btnMvp = types.InlineKeyboardButton("MVP | 210₽", callback_data="buy mvp")
    btnPrem = types.InlineKeyboardButton("Premuim | 60₽", callback_data="buy premuim")
    
    markup.add(btnMvp, btnPrem)
    
    back_button = types.InlineKeyboardButton(f"Назад", callback_data=f"profile")
    markup.add(back_button)
    
    bot.edit_message_text("Выберете статус который зотите преобрести:", ch_id, message.message_id, reply_markup=markup)
   
#BackEnd 
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    if call.data == 'change_model':
        show_models(call.message)
        
    
    if call.data == 'buy_status':
        show_status(call.message)
        
    
    if call.data == 'buy mvp': 
        bot.edit_message_text("""
⭐️ Чтобы приобрести статус MVP, выполните следующие шаги:

 1. 🧐Узнайте свой никнейм. 
Главная станица телеграмма -> три полоски в левом верхнем углу -> Мой профиль ->  Зажмите пальцем поле "Имя пользователя" -> Копировать имя
 2. 📲Отправьте донат суммой 210₽ на Boosty (https://boosty.to/aurorabot/donate) с текстом:
{Ваш nickname, например @ViktorGoldFox} MVP [Комментарий (не обязательно)]
 3. 🕗Ожидайте повышение (может занять до 6 часов, в зависимости от времени суток)

🙏При трудностях, обратитесь в техническую поддержку: @ViktorGoldFox.

❤️‍🔥 Спасибо за вашу поддержку и понимание!
                              """, call.message.chat.id, call.message.message_id)   
        
    
    if call.data == 'buy_tokens': 
        bot.edit_message_text("""
⭐️ Чтобы приобрести токены, выполните следующие шаги:

 1. 🧐Узнайте свой никнейм. 
Главная станица телеграмма -> три полоски в левом верхнем углу -> Мой профиль ->  Зажмите пальцем поле "Имя пользователя" -> Копировать имя
 2. 📲Отправьте донат суммой 1 токен = 0,1₽ на Boosty (https://boosty.to/aurorabot/donate) с текстом:
{Ваш nickname, например @ViktorGoldFox} толичество токенов [Комментарий (не обязательно)]
 3. 🕗Ожидайте повышение (может занять до 6 часов, в зависимости от времени суток)

🙏При трудностях, обратитесь в техническую поддержку: @ViktorGoldFox.

❤️‍🔥 Спасибо за вашу поддержку и понимание!
                              """, call.message.chat.id, call.message.message_id) 
        
        
    if call.data == 'buy_images': 
        bot.edit_message_text("""
⭐️ Чтобы приобрести токены, выполните следующие шаги:

 1. 🧐Узнайте свой никнейм. 
Главная станица телеграмма -> три полоски в левом верхнем углу -> Мой профиль ->  Зажмите пальцем поле "Имя пользователя" -> Копировать имя
 2. 📲Отправьте донат суммой одна картина = 0,5₽ на Boosty (https://boosty.to/aurorabot/donate) с текстом:
{Ваш nickname, например @ViktorGoldFox} толичество картин [Комментарий (не обязательно)]
 3. 🕗Ожидайте повышение (может занять до 6 часов, в зависимости от времени суток)

🙏При трудностях, обратитесь в техническую поддержку: @ViktorGoldFox.

❤️‍🔥 Спасибо за вашу поддержку и понимание!
                              """, call.message.chat.id, call.message.message_id) 
          
    
    if call.data == 'buy premuim': 
        bot.edit_message_text("""
⭐️ Чтобы приобрести статус MVP, выполните следующие шаги:

 1. 🧐Узнайте свой никнейм. 
Главная станица телеграмма -> три полоски в левом верхнем углу -> Мой профиль ->  Зажмите пальцем поле "Имя пользователя" -> Копировать имя
 2. 📲Отправьте донат суммой 60₽ на Boosty (https://boosty.to/aurorabot/donate) с текстом:
{Ваш nickname, например @ViktorGoldFox} premuim [Комментарий (не обязательно)]
 3. 🕗Ожидайте повышение (может занять до 6 часов, в зависимости от времени суток)

🙏При трудностях, обратитесь в техническую поддержку: @ViktorGoldFox.

❤️‍🔥 Спасибо за вашу поддержку и понимание!
                              """, call.message.chat.id, call.message.message_id)
    
    
    if call.data.split()[0] == 'change':
        DataBase.changeModel(call.message, model=call.data.split()[1])
        
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(f"Назад", callback_data=f"profile")
        markup.add(back_button)
    
        bot.edit_message_text(f"Модель {call.data.split()[1]} успешно применина", call.message.chat.id, call.message.message_id, reply_markup=markup)
        
    
    if call.data == 'profile':
        profile(call.message, isBack=True)
        
        # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

@bot.message_handler(func=lambda message: str(message.chat.id) == gp_id, content_types=['text'])
def write_chat_history(message):
    if True:
        message_text = str(message.text)
        message_username = str(message.from_user.username)
        save_text = str(message_username + ":" + message_text + '\n')
        with open("DataWrames/HistoryData.txt", 'a', encoding='utf-8') as file:
            file.write(str(save_text))
        file.close()

def send_error(bot_ms, error_text):
    bot.edit_message_text(chat_id=bot_ms.chat.id, message_id=bot_ms.message_id, text=error_text)
    sleep(5)
    bot.delete_message(bot_ms.chat.id, message_id=bot_ms.message_id)
    
    logger.error(error_text)

#everys
def checkbr(NowDay=0,NowMonth=0):
    # try:
    if True:
        NowDate = datetime.now()
        NowDay = NowDate.day
        NowMonth = NowDate.month
        
        print(0)
            
        nicknames, names = DataBase.checkBirthday(NowDay, NowMonth)
        
        ind = 0
        for i in range(len(nicknames)):
            text = f"Доброго дня! Сегодня день рождения у {nicknames[i]}, пожелаем {names[i]} удачи, счастья, отличного настроения и всего наилучшего!\n"
            bot.send_message(gp_id, "–=–=–=–=–=–=–=–=–=–=–=–\n" + text + "–=–=–=–=–=–=–=–=–=–=–=–")
            
            ind += 1
            
    # except Exception as e:
    #     logger.error(f"Ошибка в поздравление пользователя")   
    
    
def load_config():
    global base_model, technical_brake, usage_ask, usage_gen, global_time_work
    base_model, technical_brake, usage_ask, usage_gen = BackGround.config.loadConfig()
    
    logger.info("Конфиг успешно загружен!")


def exit():
    BackGround.config.pushConfig(technical_brake, usage_ask, usage_gen)
       
      
def send_weather():
    try:
        weather_text = BackGround.weather.GetWeather(sity = "Санкт-петербург")
        
        text = (f"Доброе утро, Петербуржцы! \n{weather_text}")

        #Отправка в группу
        bot.send_message(gp_id,text)
        
        logger.info(f'Погода в 8:00 успешно отправленна')
    
    except Exception as e:
        logger.error(f'Ошибка в погоде. Код: {e}') 
       
       
def treager():
    while True:
        schedule.run_pending()
        sleep(1)
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶ 
if __name__ == "__main__":
    schedule.every().sunday.at("00:00").do(DataBase.giveAllTokens)
    schedule.every().day.at("00:01").do(DataBase.RestartStatus)
    schedule.every().day.at("10:00").do(checkbr)
    schedule.every().day.at("08:00").do(send_weather)
    
    threading_treager = threading.Thread(target=treager)
    threading_treager.start()
    
    print("""
 ░█████╗░██╗░░░██╗██████╗░░█████╗░██████╗░░█████╗░ 
 ██╔══██╗██║░░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗ 
 ███████║██║░░░██║██████╔╝██║░░██║██████╔╝███████║ 
 ██╔══██║██║░░░██║██╔══██╗██║░░██║██╔══██╗██╔══██║ 
 ██║░░██║╚██████╔╝██║░░██║╚█████╔╝██║░░██║██║░░██║ 
 ╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝
              """)
    load_config()
    # try:
    if True:
        logger.info("Бот успешно запущен!")

        # bot.infinity_polling()
        try:
            bot.polling(non_stop=True, interval=1)
        except KeyboardInterrupt:
            
            exit(0)
        
    # except Exception as error_code:
        # logger.error(f"Ошибка хостирования бота! \nКод: {error_code}")

