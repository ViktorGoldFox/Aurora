#===================================================#
# ░█████╗░██╗░░░██╗██████╗░░█████╗░██████╗░░█████╗░ #
# ██╔══██╗██║░░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗ #
# ███████║██║░░░██║██████╔╝██║░░██║██████╔╝███████║ #
# ██╔══██║██║░░░██║██╔══██╗██║░░██║██╔══██╗██╔══██║ #
# ██║░░██║╚██████╔╝██║░░██║╚█████╔╝██║░░██║██║░░██║ #
# ╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝ #
#===================================================#

from os import error
from time import sleep
from logzero import logger, logfile

from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import telebot

import Dependencies.BackGround as BackGround
import Dependencies.DataBase as DataBase

#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
# Bot_config
bot_token = "6904577368:AAHMjsneMF0HaLHiWa08Bv2ZzBZOwIJ7yTo" #Aurora
# bot_token = "6601620934:AAGvgH9rDE4JHrUBThkrXrca9zfJIpMeh0Q" #BotTest
        # main        # second
admins = [1746901164, 1018366370]
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
# Logs
logfile("logs/logs.log")
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
usage_ask = 0
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
# Config
bot = telebot.TeleBot(bot_token)
# data = pd.read_csv("DateFrame.csv")
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶
Censored_path = "Add-ons/censored.png"
#FrontEnd
@bot.message_handler(commands=["/help"])
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
    logger.info(f"@{message.from_user.username} вывел start!")
    bot.send_message(message.chat.id, f"Привет! Я - нейросетевой бот AuroraBot {version}, и я здесь, чтобы повеселиться. Я могу помочь тебе в разных задачах /help. Я люблю общаться с людьми и узнавать что-то новое. Давай пообщаемся!")

#add
@bot.message_handler(commands=["profile"])
def profile(message, isBack=False):
    if BackGround.chenkChatType(message): bot.send_message(message.chat.id, "❌Напиши команду боту в личные сообщения"); return False
    
    if str(message.chat.type) != 'private': bot.send_message(message.chat.id, "❌Напиши команду боту в личные сообщения")
    
    if (technical_brake) & (message.chat.id not in admins): 
        bot.send_message(message.chat.id, "❌Идут тех. работы! Попробуйте позже!")
        return False
        
    profile_data = DataBase.get_profile(message, bot.get_chat_member(gp_id, message.from_user.id).status)
    
    if not isBack:
        DataBase.check.CurentNickname(message)
    
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


@bot.message_handler(commands=["add"])
def add(message):
    ch_id = message.chat.id
    
    if str(message.chat.type) != 'private': bot.send_message(message.chat.id, "❌Напиши команду боту в личные сообщения")
    
    if (technical_brake) & (message.chat.id not in admins): 
        bot.send_message(message.chat.id, "❌Идут тех. работы! Попробуйте позже!")
        return False
    
    if bot.get_chat_member(gp_id, message.from_user.id).status == 'left': 
        bot.send_message(message.chat.id, text="❌Вы не являетесь участником группы.")
        return False
    
    if message.text.split()[0] != '/add':
        if BackGround.checkCanceled(message.text): bot.send_message(ch_id, "Отменил!")
    
        addResualt = BackGround.addNewUser(message)

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

        weather_text = BackGround.GetForecast(sity)

        weather_text = BackGround.markdown_convert(weather_text)
        
        bot.edit_message_text(weather_text, message.chat.id, loading_message.message_id, parse_mode="MarkdownV2" )

        logger.info(f"@{message.from_user.username} вывел прогноз погоды")
        
    except Exception as error:
        logger.error(f"Ошибка в погоде: {error}") 
        send_error(loading_message, "❌В названии города ошибка. Попробуйте снова!")
        

@bot.message_handler(commands=["weather"])
def weather(message):
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

        weather_text = BackGround.GetWeather(sity)

        bot.edit_message_text(weather_text, message.chat.id, loading_message.message_id, parse_mode="MarkdownV2")

        logger.info(f"@{message.from_user.username} вывел погоду")
        
    except Exception as error:
        logger.error(f"Ошибка в погоде: {error}") 
        send_error(loading_message, "❌В названии города ошибка. Попробуйте снова!")


@bot.message_handler(commands=["sum"])
def sum(message):
    # try:
        loading_mess = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше сообщение обрабатывается")
        loading_mess
        
        logger.info(f"@{message.from_user.username} Начал запрос gpt")
        
        ch_id = message.chat.id
        
        # Проверка на техничесские работы
        if (technical_brake) & (message.chat.id not in admins): 
            bot.edit_message_text("❌Идут тех. работы! Попробуйте позже!", ch_id, loading_mess.message_id)
            return False
        # Проверка на участника группы
        if bot.get_chat_member(gp_id, message.from_user.id).status == 'left': 
            bot.send_message(message.chat.id, text="❌Вы не являетесь участником группы.")
            return False
        # Проверка на свежость запроса
        if BackGround.freshcheck(message, fresh_time): 
            send_error(bot_ms=loading_mess, error_text="❌Запрос устарел. Попробуйте снова!")
            return False
        # Проверка на то что у пользователя есть никнейм
        if message.from_user.username == None: 
            send_error(bot_ms=loading_mess, error_text="❌Прежде чем использовать комманду /ask, надо установить никнейм!")
            return False
            
        summorysen_coll = BackGround.GetSummorysenNumber(message)
        
        if BackGround.CheckSumNumberInRange(summorysen_coll):
            send_error(loading_mess.message_id, text="❌Значения для суммирования: 50,100,150,350. Попробуйте снова.")
            return False
        
        get_text = BackGround.GetLines(summorysen_coll)
        
        promt = f'Суммируй эти сообщения обязательно с упоминанием пользователей и что они писали кратко и обрабатывая каждое сообщение не списком а целым текстом без общей темы в конце и с капелькой дичи объем: 0.5 страниц: {get_text}'
        if summorysen_coll <= 100:
            promt = f'Суммируй эти сообщения обязательно с упоминанием пользователей и что они писали обрабатывая каждое сообщение не списком а целым текстом без общей темы в концеи с капелькой дичи  объем: 1 страниц: {get_text}'
        if summorysen_coll >= 150:
            promt = f'Суммируй эти сообщения обязательно с упоминанием пользователей и что они писали обрабатывая каждое сообщение не списком а целым текстом без общей темы в конце и с капелькой дичи  очееень длинно и развернуто в 10 страниц: {get_text}'
            
        summorysen_text = BackGround.askGPT(promt, "gpt-3.5-turbo-0125", token=open_ai_token)
        summorysen_text = str(f"Aurora-{version} - Последние {summorysen_coll} cообщений суммированны так: \n{summorysen_text}")
        
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("❤️Поддержать автора", url=donate_url)
        markup.add(btn)
        
        bot.edit_message_text(chat_id=message.chat.id, message_id=loading_mess.message_id, text=str(summorysen_text))
        
        logger.info(f'@{message.from_user.username} суммировал {summorysen_coll} сообщений')
        
    # except Exception as error:
        # logger.error(f"Ошибка sum \nКод: {error}")
        # 
        # return False


@bot.message_handler(commands=["ask", "gpt"])
def ask(message, chat_is_local = True):
    global usage_ask
    if True:
    # try:
        loading_mess = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше сообщение обрабатывается")
        loading_mess
        
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
        
        user_gpt_model = DataBase.getCurrentModel(message)
        if user_gpt_model in ["gpt-4-turbo", 'gpt-4-turbo-24-04-09', "gpt-4-1106-preview"]:
            usage_tokens = BackGround.mathToken(text=user_promt, is_gpt4=True)
        else:
            usage_tokens = BackGround.mathToken(text=user_promt)
            
        # Проверка наличия ответа на сообщение
        if message.reply_to_message != None: user_promt = f"{user_promt}: {message.reply_to_message.text}"
        
        if DataBase.check.tokens_ask(message, usage_tokens):
            bot.edit_message_text("❌Недостаточно токенов! Для покупки писать сюда - @ViktorGoldFox", message.chat.id, loading_mess.message_id)
            return False
        
        if message.chat.id != gp_id:
            DataBase.check.add_user(message, bot.get_chat_member(gp_id, message.from_user.id).status)
        
        DataBase.subtraction_tokens.ask(message, usage_tokens)
        
        answer_text = BackGround.askGPT(user_promt, user_gpt_model, open_ai_token)
        
        if DataBase.check.ShowLastToken(message, gp_id): 
            ms_text = f"{BackGround.markdown_convert(answer_text)} \n{BackGround.GetLastTokens(message, usage_tokens, DataBase.get_last_tokens(message))}"
        
        ms_text = f"{BackGround.markdown_convert(answer_text)}"
        
        if (usage_ask % ask_coll) == 0:
            markup = types.InlineKeyboardMarkup()
            btn_adv = types.InlineKeyboardButton("❤️Поддержать автора", url=donate_url)
            markup.add(btn_adv)
            bot.edit_message_text(f"""{ms_text}""", ch_id, loading_mess.message_id, reply_markup=markup, parse_mode='MarkdownV2')
        else:
            bot.edit_message_text(f"""{ms_text}""", ch_id, loading_mess.message_id, parse_mode='MarkdownV2')
            
        usage_ask += 1
        
        logger.info(f"@{message.from_user.username} Использовал GPT \nPromt: {user_promt} \nAverage: {answer_text} \nTokens: {usage_tokens}")
    # except Exception as error:
    #     logger.error(f"Ошибка GPT \nКод: {error}")
        
    #     return False
        

@bot.message_handler(commands=["gen", "generate", "image"])
def generate(message):
    global usage_gen
    try:
        loading_mess = bot.send_message(message.chat.id, "🕐 Подождите несколько секунд. Ваше сообщение обрабатывается")
        loading_mess
        
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
            bot.edit_message_text("❌Недостаточно токенов! Для покупки писать сюда - @ViktorGoldFox", message.chat.id, loading_mess.message_id)
            return False
        
        GenImagesData = BackGround.ImageGenerator(promt=user_promt)
        model_id = BackGround.GetKandiskyModel()
        
        if BackGround.CheckLenImages(images=GenImagesData):
            send_error(bot_ms=loading_mess, error_text="❌Долгий ответ сервера. Попробуйте снова!")
            return False
        
        if BackGround.CheckCensored(images=GenImagesData):
            with open(Censored_path, 'rb') as image:
                bot.send_photo(ch_id, image, caption="❌Промт зацензурен. Генерация невозможна")
                bot.delete_message(ch_id, loading_mess.message_id)
                
                return False
        
        BackGround.NotAvailabilityUser(message, gp_id=gp_id, user_status=bot.get_chat_member(gp_id, message.from_user.id).status)
        DataBase.subtraction_tokens.gen(message)
        
        generatedImage = BackGround.ConvertImage(GenImagesData['images'][0])
        
        if usage_gen % gen_coll == 0:
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("❤️Поддержать автора", url=donate_url)
            markup.add(btn)
            
            if BackGround.CheckShowLastToken(message, gp_id):
                bot.send_photo(message.chat.id, generatedImage, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово {BackGround.GetLastImages(message, DataBase.get_last_images(message))}"), reply_markup=markup)
            else:
                bot.send_photo(message.chat.id, generatedImage, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово"), reply_markup=markup)
        else:
            if BackGround.CheckShowLastToken(message, gp_id):
                bot.send_photo(message.chat.id, generatedImage, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово {BackGround.GetLastImages(message, DataBase.get_last_images(message))}"))
            else:
                bot.send_photo(message.chat.id, generatedImage, caption=str(f"✅Kandinsky{model_id} - @{message.from_user.username}, ваше изображение готово"), reply_markup=markup)
                
        bot.delete_message(message.chat.id, message_id=loading_mess.message_id)
        
        usage_gen += 1
        
    except Exception as error:
        logger.error(f"Ошибка GPT \nКод: {error}")
        
        return False

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
    # if call.data == 'change_model':
    #     show_models(call.message)
        
    # if call.data == 'change_model':
    #     show_models(call.message)
    
    if call.data.split()[0] == 'change':
        DataBase.changeModel(call.message, model=call.data.split()[1])
        
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(f"Назад", callback_data=f"profile")
        markup.add(back_button)
    
        bot.edit_message_text(f"Модель {call.data.split()[1]} успешно применина", call.message.chat.id, call.message.message_id, reply_markup=markup)
        
    
    if call.data == 'profile':
        profile(call.message, isBack=True)
        
        # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    

def send_error(bot_ms, error_text):
    bot.edit_message_text(chat_id=bot_ms.chat.id, message_id=bot_ms.message_id, text=error_text)
    sleep(5)
    bot.delete_message(bot_ms, message_id=bot_ms.message_id)
    
    logger.error(error_text)
    
    
def load_config():
    global base_model, technical_brake, usage_ask, usage_gen
    base_model, technical_brake, usage_ask, usage_gen = BackGround.loadConfig()
    
    logger.info("Конфиг успешно загружен!")
       
#=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶=̶ 
if __name__ == "__main__":
    load_config()
    # try:
    if True:
        print("""
 ░█████╗░██╗░░░██╗██████╗░░█████╗░██████╗░░█████╗░ 
 ██╔══██╗██║░░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗ 
 ███████║██║░░░██║██████╔╝██║░░██║██████╔╝███████║ 
 ██╔══██║██║░░░██║██╔══██╗██║░░██║██╔══██╗██╔══██║ 
 ██║░░██║╚██████╔╝██║░░██║╚█████╔╝██║░░██║██║░░██║ 
 ╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝
              """)
        logger.info("Бот успешно запущен!")
        
        # bot.infinity_polling()
        bot.polling(non_stop=True, interval=1)
        
    # except Exception as error_code:
        # logger.error(f"Ошибка хостирования бота! \nКод: {error_code}")

