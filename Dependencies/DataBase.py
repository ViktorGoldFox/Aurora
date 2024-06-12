import pandas as pd

#*Codes:
#! 401 - user not subcrige
#! 200 - User in premuim
#! 201 - Created
#! 202 - accept
#! 402 - Many tokens 

chatid = '-1001665880322'

mvp_models = ["gpt-4-turbo", 'gpt-4-turbo-24-04-09', "gpt-4-1106-preview", "gpt-4o-2024-05-13"]
premuim_models = ["gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k"]
default_models = ["gpt-3.5-turbo-0613", "gpt-3.5-turbo-0914"]

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
                return 401


    def add_user(message, member_status):

            datauser = pd.read_csv(user_data_path)

            if datauser[datauser['chat_id'] == message.chat.id].shape[0] == 0:

                if member_status == 'left':
                    append_data = f"\n{message.from_user.username},{message.chat.id},default,250"
                else:
                    append_data = f"\n{message.from_user.username},{message.chat.id},group,0"

                with open(user_data_path, 'a') as csv:
                    csv.write(f"{append_data}")
                    csv.close()

                return 200
    
    
    def ShowLastToken(chat_id, gp_id):
        datauser = pd.read_csv(user_data_path)

        index = datauser.index[datauser['chat_id'] == chat_id][0]
        
        if (str(datauser.loc[index, "status"]) not in ['admin', 'group']) | chat_id == gp_id:
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
    
    
def get_profile(message): #, member_status):
    mess_id = message.chat.id
    # if check.NotAvailabilityUser(mess_id): check.add_user(message, member_status)
    
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
        
        case "default": return default_models
        
        
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
    datauser.to_csv(user_data_path, index=False)
    
    return f"✅Успешно установлен статус {setStatusName} пользователю {userName}"


def setTokens(userName, tokenColl):
    datauser = pd.read_csv(user_data_path)
    
    index = datauser.index[datauser['name'] == userName][0]
    
    datauser.loc[index, "tokens"] = tokenColl
    datauser.to_csv(user_data_path, index=False)
    
    return f"✅Успешно установленно {tokenColl} токенов пользователю {userName}"


def giveTokens(userName, tokenColl):
    datauser = pd.read_csv(user_data_path)
    
    index = datauser.index[datauser['name'] == userName][0]
    
    datauser.loc[index, "tokens"] = int(datauser.loc[index, "tokens"]) + tokenColl
    datauser.to_csv(user_data_path, index=False)
    
    return f"✅Успешно выдано {tokenColl} токенов пользователю {userName}"


def setImage(userName, imagesColl):
    datauser = pd.read_csv(user_data_path)
    
    index = datauser.index[datauser['name'] == userName][0]
    
    datauser.loc[index, "images"] = imagesColl
    datauser.to_csv(user_data_path, index=False)
    
    return f"✅Успешно установленно {imagesColl} картин пользователю {userName}"


def setImage(userName, imagesColl):
    datauser = pd.read_csv(user_data_path)
    
    index = datauser.index[datauser['name'] == userName][0]
    
    datauser.loc[index, "images"] = int(datauser.loc[index, "images"]) + imagesColl
    datauser.to_csv(user_data_path, index=False)
    
    return f"✅Успешно выданно {imagesColl} картин пользователю {userName}"