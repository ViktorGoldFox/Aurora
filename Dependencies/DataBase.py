import pandas as pd
from datetime import datetime

#*Codes:
#! 401 - user not subcrige
#! 200 - User in premuim
#! 201 - Created
#! 202 - accept
#! 402 - Many tokens 

chatid = '-1001665880322'

mvp_models = ["gpt-4-turbo", 'gpt-4-turbo-24-04-09', "gpt-4-1106-preview", "gpt-4o-2024-05-13"]
premuim_models = ["gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k"]
default_models = ["gpt-3.5-turbo-0613"]

user_data_path = "DataWrames/UsersData.csv"

class check:
    def CurentNickname(message):
        datauser = pd.read_csv(user_data_path)

        if datauser[datauser['name'] == message.from_user.username].shape[0] == 0:
            index = datauser.index[datauser['chat_id'] == message.chat.id][0]
            
            datauser.at[index, 'name'] = message.from_user.username
            
            datauser.to_csv(user_data_path, index=False)
            
    
    def NotAvailabilityUser(user_chat_id) -> bool:
        datauser = pd.read_csv(user_data_path)
        if datauser[datauser['chat_id'] == user_chat_id].shape[0] == 0: return True
        else: return False
        
    def subscribe(message, member_status):
        if (str(message.chat.id) != chatid) & (str(message.chat.id) != '1467854871'):
            if member_status == 'left':
                return True
        
        return False


    def add_user(message, member_status):

            datauser = pd.read_csv(user_data_path)

            if datauser[datauser['chat_id'] == message.chat.id].shape[0] == 0:

                if member_status == 'left':
                    append_data = f"\n{message.from_user.username},{message.chat.id},default,250,15,gpt-3.5-turbo-0613,0"
                else:
                    append_data = f"\n{message.from_user.username},{message.chat.id},group,0,0,gpt-3.5-turbo-0613,0"

                with open(user_data_path, 'a') as csv:
                    csv.write(f"{append_data}")
                    csv.close()

                return 200
    
    
    def ShowLastToken(chat_id, gp_id):
        datauser = pd.read_csv(user_data_path)

        index = datauser.index[datauser['chat_id'] == chat_id][0]
        
        if (str(datauser.loc[index, "status"]) not in ['admin', 'group']) | chat_id != gp_id:
            return True
        else:
            return False
    

    def images_gen(message):
        
        datauser = pd.read_csv(user_data_path)
        
        index = datauser.index[datauser['chat_id'] == message.chat.id][0]
        
        if str(datauser.loc[index, "status"]) not in ['admin', 'group']:
            if datauser.loc[index, "tokens"] < 1:
                return True
            
        return False
            
    
    def user(user_name):
        user_name = str(user_name).replace("@", "")
        
        datauser = pd.read_csv(user_data_path)
        
        if datauser[datauser['name'] == user_name].shape[0] == 0:
            return "❌ Пользователь не найден"
        else:
            index = datauser.index[datauser['name'] == user_name][0]

            return datauser.loc[index, "chat_id"]
            
    
    
    def tokens_ask(message, use_tokens):
    
        datauser = pd.read_csv(user_data_path)
        
        index = datauser.index[datauser['chat_id'] == message.chat.id][0]
        
        if str(datauser.loc[index, "status"]) not in ['admin', 'group']:
            if datauser.loc[index, "tokens"] < use_tokens:
                return True
            
        return False
            
            
class subtraction_tokens():
    def gen(message):
        if str(message.chat.id) != chatid:
            datauser = pd.read_csv(user_data_path)
            index = datauser.index[datauser['chat_id'] == message.chat.id][0]
            
            if str(datauser.loc[index, 'status']) not in ['admin', 'group']:
                if message.chat.id != chatid:
                    datauser.loc[index, "images"] = int(datauser.loc[index, "images"]) - 1
                    datauser.to_csv(user_data_path, index=False)
                    return 202
            else:
                return 200
            
            
    def ask(message, use_tokens):
        if str(message.chat.id) != chatid:
            
            datauser = pd.read_csv(user_data_path)
            index = datauser.index[datauser['chat_id'] == message.chat.id][0]
            
            if str(datauser.loc[index, 'status']) not in ['admin', 'group']:
                if message.chat.id != chatid:
                    datauser.loc[index, "tokens"] = int(datauser.loc[index, "tokens"]) - (use_tokens * 5)
                    datauser.to_csv(user_data_path, index=False)
                    return 202
                
                
def get_last_tokens(message):
    datauser = pd.read_csv(user_data_path)
    index = datauser.index[datauser['chat_id'] == message.chat.id][0]
    
    if str(datauser.loc[index, "status"]) not in ['admin', 'group']:
        last_tokens = datauser.loc[index, "tokens"]
    else:
        last_tokens = "∞"
    return last_tokens


def get_last_images(message):
    datauser = pd.read_csv(user_data_path)
    index = datauser.index[datauser['chat_id'] == message.chat.id][0]
    
    if str(datauser.loc[index, "status"]) not in ['admin', 'group']:
        last_images = datauser.loc[index, "images"]
    else:
        last_images = "∞"
    return last_images
    
    
def get_profile(message, member_status):
    mess_id = message.chat.id
    if check.NotAvailabilityUser(mess_id): check.add_user(message, member_status)
    
    datauser = pd.read_csv(user_data_path)
    
    index = datauser.index[datauser['chat_id'] == message.chat.id][0]
    name = datauser.loc[index, "name"]
    status = datauser.loc[index, "status"]
    tokens = datauser.loc[index, "tokens"]
    model = datauser.loc[index, "model"]
    images = datauser.loc[index, "images"]
    
    if str(status) in ['admin','group']: 
        tokens = '∞'
        images = '∞'
    
    return [name, status, tokens, model, images]
    

def getCurrentModel(message):
    datauser = pd.read_csv(user_data_path)
    
    index = datauser.index[datauser['chat_id'] == message.chat.id][0]
    return datauser.loc[index, "model"]


def get_models(message_chatId):
    datauser = pd.read_csv(user_data_path)
    
    index = datauser.index[datauser['chat_id'] == message_chatId][0]
    status = datauser.loc[index, "status"]
    
    match status:
        case "mvp" | "admin":
            models = mvp_models + premuim_models + default_models
            
            return models
        
        case "premuim":
            models = premuim_models + default_models
            
            return models
        
        case "default" | "group": return default_models
        
        
def changeModel(message, model):
    datauser = pd.read_csv(user_data_path)
    
    index = datauser.index[datauser['chat_id'] == message.chat.id][0]
    
    datauser.at[index, 'model'] = model
            
    datauser.to_csv(user_data_path, index=False)
    
    
def setStatus(userName, setStatusName):
    datauser = pd.read_csv(user_data_path)
    
    if setStatusName not in ["premuim", "mvp", "admin", "default", "group"]: 
        return "❌Неверное имя статуса"
    index = datauser.index[datauser['name'] == userName][0]
    
    datauser.loc[index, "status"] = str(setStatusName)
    match str(setStatusName):
        case "default":
            datauser.loc[index, "tokens"] = 1000
            datauser.loc[index, "images"] = 15
        case "premuim":
            datauser.loc[index, "tokens"] = 50000
            datauser.loc[index, "images"] = 45
        case "mvp":
            datauser.loc[index, "tokens"] = 20000
            datauser.loc[index, "images"] = 100
    datauser.to_csv(user_data_path, index=False)
    
    return f"✅Успешно установлен статус {setStatusName} пользователю {userName}"


def setTokens(userName, tokenColl):
    datauser = pd.read_csv(user_data_path)
    
    index = datauser.index[datauser['name'] == userName][0]
    
    datauser.loc[index, "tokens"] = int(tokenColl)
    datauser.to_csv(user_data_path, index=False)
    
    return f"✅Успешно установленно {tokenColl} токенов пользователю {userName}"


def giveTokens(userName, tokenColl):
    datauser = pd.read_csv(user_data_path)
    
    if datauser[datauser['name'] == userName].shape[0] == 0: return "❌ Пользователь не найден"
    
    index = datauser.index[datauser['name'] == userName][0]
    
    datauser.loc[index, "tokens"] = int(datauser.loc[index, "tokens"]) + int(tokenColl)
    datauser.to_csv(user_data_path, index=False)
    
    return f"✅Успешно выдано {tokenColl} токенов пользователю {userName}"


def setImage(userName, imagesColl):
    datauser = pd.read_csv(user_data_path)
    
    index = datauser.index[datauser['name'] == userName][0]
    
    datauser.loc[index, "images"] = int(imagesColl)
    datauser.to_csv(user_data_path, index=False)
    
    return f"✅Успешно установленно {imagesColl} картин пользователю {userName}"


def giveImage(userName, imagesColl):
    datauser = pd.read_csv(user_data_path)
    
    index = datauser.index[datauser['name'] == userName][0]
    
    datauser.loc[index, "images"] = int(datauser.loc[index, "images"]) + int(imagesColl)
    datauser.to_csv(user_data_path, index=False)
    
    return f"✅Успешно выданно {imagesColl} картин пользователю {userName}"


def checkBirthday(NowDay,NowMonth):
    data = pd.read_csv("DataWrames/Birthdays.csv")
        
    if int(data[(data['dday'] == NowDay) & (data["dmon"] == NowMonth)].shape[0]) <= 0: return False
    
    NowDR = []
    if int(data[(data['dday'] == NowDay) & (data["dmon"] == NowMonth)].shape[0]) >= 1:
        NowDR = data.index[(data['dday'] == NowDay) & (data["dmon"] == NowMonth)].tolist()
        
    print(NowDR)
    
    ind = 0
    nicknames = []
    names = []
    for ind in range(len(NowDR)):
        print(ind)
        
        nicknames.append(data.loc[NowDR[ind],"nickname"])
        names.append(data.loc[NowDR[ind],"Username"])
                
        print(nicknames, names)
        
        ind += 1
        
    return nicknames, names
    

def giveAllTokens():
    datauser = pd.read_csv("DataWrames/UsersData.csv")
    
    for index in range(datauser.shape[0]):
        match str(datauser.loc[index, 'status']):
            case "default":
                datauser.loc[index, "tokens"] = int(datauser.loc[index, "tokens"]) + max(int(1000 - datauser.loc[index, "tokens"]), 0)
                datauser.loc[index, "images"] = int(datauser.loc[index, "images"]) + max(int(15 - datauser.loc[index, "images"]), 0)
                datauser.loc[index, "model"] = "gpt-3.5-turbo-0613"
            case "premuim":
                datauser.loc[index, "tokens"] = int(datauser.loc[index, "tokens"]) + max(int(5000 - datauser.loc[index, "tokens"]), 0)
                datauser.loc[index, "images"] = int(datauser.loc[index, "images"]) + max(int(45 - datauser.loc[index, "images"]), 0)
            case "mvp":
                datauser.loc[index, "tokens"] = int(datauser.loc[index, "tokens"]) + max(int(20000 - datauser.loc[index, "tokens"]), 0)
                datauser.loc[index, "images"] = int(datauser.loc[index, "images"]) + max(int(100 - datauser.loc[index, "images"]), 0)
            
    datauser.to_csv('DataWrames/UsersData.csv', index=False)


def RestartStatus():
    datauser = pd.read_csv("DataWrames/UsersData.csv")
    
    for index in range(datauser.shape[0]):
        if str(datetime.now()).split()[0] == datauser.loc[index, "end_time"]:
            datauser.loc[index, "end_time"] = 0
            datauser.loc[index, "status"] = "default"
            datauser.loc[index, "tokens"] = 1000
            datauser.loc[index, "images"] = 15
            
            datauser.to_csv('DataWrames/UsersData.csv', index=False)
            